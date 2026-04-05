from flask import Flask
from models import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chave_secreta_super_segura_2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    from routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
