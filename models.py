from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from datetime import datetime
import re

db = SQLAlchemy()
login_manager = LoginManager()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    foto = db.Column(db.String(255), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'foto': self.foto,
            'data_cadastro': self.data_cadastro.strftime("%d/%m/%Y %H:%M") if self.data_cadastro else None
        }

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def validar_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validar_senha(senha):
    if len(senha) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres"
    if not re.search(r"\d", senha):
        return False, "Senha deve ter pelo menos 1 número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "Senha deve ter pelo menos 1 caractere especial (!@#$%...)"
    return True, ""
