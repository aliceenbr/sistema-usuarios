import pytest
from app import create_app
from models import db, Usuario

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def usuario(app):
    with app.app_context():
        user = Usuario(nome='Teste', email='teste@teste.com')
        user.set_senha('Teste@123')
        db.session.add(user)
        db.session.commit()
        return user.id

@pytest.fixture
def usuario_logado(client, usuario):
    client.post('/login', data={
        'email': 'teste@teste.com',
        'senha': 'Teste@123'
    }, follow_redirects=True)
    return usuario
