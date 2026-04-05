import os
import logging
from flask import Flask
from models import db, login_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_secreta_fallback')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cadastro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    from routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api)
    
    logger.info('Inicializando aplicacao...')
    
    with app.app_context():
        db.create_all()
        
        uploads_path = os.path.join(app.root_path, 'static', 'uploads')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
            logger.info('Pasta uploads criada')
    
    logger.info('Aplicacao iniciada com sucesso')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
