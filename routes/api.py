from flask import jsonify, request
from flask_login import login_required, current_user
from models import Usuario

@api.route('/usuarios', methods=['GET'])
@login_required
def api_listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return jsonify({
        'sucesso': True,
        'total': len(usuarios),
        'usuarios': [u.to_dict() for u in usuarios]
    })

@api.route('/usuarios/<int:id>', methods=['GET'])
@login_required
def api_buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({
            'sucesso': False,
            'erro': 'Usuário não encontrado'
        }), 404
    
    return jsonify({
        'sucesso': True,
        'usuario': usuario.to_dict()
    })

@api.route('/usuarios', methods=['POST'])
@login_required
def api_criar_usuario():
    from models import validar_email, validar_senha
    from models import db
    
    dados = request.get_json()
    
    nome = dados.get('nome', '').strip()
    email = dados.get('email', '').strip()
    senha = dados.get('senha', '')
    
    if not nome or not email or not senha:
        return jsonify({
            'sucesso': False,
            'erro': 'Preencha todos os campos'
        }), 400
    
    if not validar_email(email):
        return jsonify({
            'sucesso': False,
            'erro': 'Email inválido'
        }), 400
    
    if Usuario.query.filter_by(email=email).first():
        return jsonify({
            'sucesso': False,
            'erro': 'Email já cadastrado'
        }), 400
    
    valida, erro = validar_senha(senha)
    if not valida:
        return jsonify({
            'sucesso': False,
            'erro': erro
        }), 400
    
    novo_usuario = Usuario(nome=nome, email=email)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Usuário criado com sucesso',
        'usuario': novo_usuario.to_dict()
    }), 201

@api.route('/usuarios/<int:id>', methods=['PUT'])
@login_required
def api_atualizar_usuario(id):
    from models import validar_email, validar_senha
    from models import db
    
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({
            'sucesso': False,
            'erro': 'Usuário não encontrado'
        }), 404
    
    dados = request.get_json()
    
    novo_nome = dados.get('nome', '').strip()
    novo_email = dados.get('email', '').strip()
    nova_senha = dados.get('senha')
    
    if not novo_nome or not novo_email:
        return jsonify({
            'sucesso': False,
            'erro': 'Nome e email são obrigatórios'
        }), 400
    
    if not validar_email(novo_email):
        return jsonify({
            'sucesso': False,
            'erro': 'Email inválido'
        }), 400
    
    email_existente = Usuario.query.filter_by(email=novo_email).first()
    if email_existente and email_existente.id != id:
        return jsonify({
            'sucesso': False,
            'erro': 'Email já está em uso'
        }), 400
    
    if nova_senha:
        valida, erro = validar_senha(nova_senha)
        if not valida:
            return jsonify({
                'sucesso': False,
                'erro': erro
            }), 400
        usuario.set_senha(nova_senha)
    
    usuario.nome = novo_nome
    usuario.email = novo_email
    db.session.commit()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Usuário atualizado com sucesso',
        'usuario': usuario.to_dict()
    })

@api.route('/usuarios/<int:id>', methods=['DELETE'])
@login_required
def api_deletar_usuario(id):
    from models import db
    
    if id == current_user.id:
        return jsonify({
            'sucesso': False,
            'erro': 'Você não pode excluir seu próprio usuário'
        }), 400
    
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({
            'sucesso': False,
            'erro': 'Usuário não encontrado'
        }), 404
    
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Usuário excluído com sucesso'
    })

@api.route('/estatisticas', methods=['GET'])
@login_required
def api_estatisticas():
    from datetime import datetime
    
    total = Usuario.query.count()
    hoje = Usuario.query.filter(
        db.func.date(Usuario.data_cadastro) == datetime.now().date()
    ).count()
    
    return jsonify({
        'sucesso': True,
        'estatisticas': {
            'total_usuarios': total,
            'cadastros_hoje': hoje
        }
    })

@api.route('/buscar', methods=['GET'])
@login_required
def api_buscar():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify({
            'sucesso': True,
            'resultados': [],
            'total': 0
        })
    
    usuarios = Usuario.query.filter(
        (Usuario.nome.ilike(f'%{termo}%')) | 
        (Usuario.email.ilike(f'%{termo}%'))
    ).order_by(Usuario.nome).all()
    
    return jsonify({
        'sucesso': True,
        'resultados': [u.to_dict() for u in usuarios],
        'total': len(usuarios)
    })
