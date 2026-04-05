from flask import render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from models import Usuario, db
from routes import main
import os
from datetime import datetime

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        
        if not email or not senha:
            flash('Preencha todos os campos!', 'erro')
            return render_template('login.html')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_senha(senha):
            from flask_login import login_user
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        
        flash('Email ou senha incorretos!', 'erro')
    
    return render_template('login.html')

@main.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        
        if not nome or not email or not senha:
            flash('Preencha todos os campos!', 'erro')
            return render_template('registrar.html')
        
        from models import validar_email, validar_senha
        
        if not validar_email(email):
            flash('Email inválido!', 'erro')
            return render_template('registrar.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este email já está cadastrado!', 'erro')
            return render_template('registrar.html')
        
        valida, erro = validar_senha(senha)
        if not valida:
            flash(erro, 'erro')
            return render_template('registrar.html')
        
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('main.login'))
    
    return render_template('registrar.html')

@main.route('/dashboard')
@login_required
def dashboard():
    total_usuarios = Usuario.query.count()
    usuarios = Usuario.query.order_by(Usuario.data_cadastro.desc()).limit(6).all()
    
    stats = {
        'total': total_usuarios,
        'hoje': Usuario.query.filter(
            db.func.date(Usuario.data_cadastro) == datetime.now().date()
        ).count()
    }
    
    return render_template('dashboard.html', usuarios=usuarios, total=total_usuarios, stats=stats)

@main.route('/usuarios/lista')
@login_required
def lista_usuarios():
    ordenar = request.args.get('ordenar', 'nome')
    usuarios = Usuario.query.order_by(
        Usuario.nome.asc() if ordenar == 'nome' else Usuario.data_cadastro.desc()
    ).all()
    return render_template('lista.html', usuarios=usuarios, total=len(usuarios))

@main.route('/usuarios/cadastrar', methods=['POST'])
@login_required
def cadastrar_usuario():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')
    
    if not nome or not email or not senha:
        flash('Preencha todos os campos!', 'erro')
        return redirect(url_for('main.dashboard'))
    
    from models import validar_email, validar_senha
    
    if not validar_email(email):
        flash('Email inválido!', 'erro')
        return redirect(url_for('main.dashboard'))
    
    if Usuario.query.filter_by(email=email).first():
        flash('Este email já está cadastrado!', 'erro')
        return redirect(url_for('main.dashboard'))
    
    valida, erro = validar_senha(senha)
    if not valida:
        flash(erro, 'erro')
        return redirect(url_for('main.dashboard'))
    
    novo_usuario = Usuario(nome=nome, email=email)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    flash('Usuário cadastrado com sucesso!', 'sucesso')
    return redirect(url_for('main.lista_usuarios'))

@main.route('/usuarios/buscar')
@login_required
def buscar():
    termo = request.args.get('q', '').strip()
    
    if termo:
        usuarios = Usuario.query.filter(
            (Usuario.nome.ilike(f'%{termo}%')) | 
            (Usuario.email.ilike(f'%{termo}%'))
        ).order_by(Usuario.nome).all()
    else:
        usuarios = []
    
    return render_template('buscar.html', usuarios=usuarios, termo=termo)

@main.route('/usuarios/perfil/<int:id>')
@login_required
def perfil(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('perfil.html', usuario_perfil=usuario)

@main.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        novo_nome = request.form.get('nome', '').strip()
        novo_email = request.form.get('email', '').strip()
        nova_senha = request.form.get('senha', '').strip()
        
        from models import validar_email, validar_senha
        
        if not novo_nome or not novo_email:
            flash('Preencha os campos obrigatórios!', 'erro')
            return redirect(url_for('main.editar', id=id))
        
        if not validar_email(novo_email):
            flash('Email inválido!', 'erro')
            return redirect(url_for('main.editar', id=id))
        
        email_existente = Usuario.query.filter_by(email=novo_email).first()
        if email_existente and email_existente.id != id:
            flash('Este email já está em uso!', 'erro')
            return redirect(url_for('main.editar', id=id))
        
        if nova_senha:
            valida, erro = validar_senha(nova_senha)
            if not valida:
                flash(erro, 'erro')
                return redirect(url_for('main.editar', id=id))
            usuario.set_senha(nova_senha)
        
        usuario.nome = novo_nome
        usuario.email = novo_email
        db.session.commit()
        
        flash('Usuário atualizado com sucesso!', 'sucesso')
        return redirect(url_for('main.perfil', id=id))
    
    return render_template('editar.html', usuario_edit=usuario)

@main.route('/usuarios/foto/<int:id>', methods=['POST'])
@login_required
def upload_foto(id):
    usuario = Usuario.query.get_or_404(id)
    
    if 'foto' not in request.files:
        flash('Nenhuma imagem selecionada!', 'erro')
        return redirect(url_for('main.editar', id=id))
    
    arquivo = request.files['foto']
    
    if arquivo.filename == '':
        flash('Nenhuma imagem selecionada!', 'erro')
        return redirect(url_for('main.editar', id=id))
    
    if arquivo:
        extensao = arquivo.filename.rsplit('.', 1)[1].lower() if '.' in arquivo.filename else ''
        if extensao not in ['jpg', 'jpeg', 'png', 'gif']:
            flash('Apenas imagens JPG, PNG ou GIF são permitidas!', 'erro')
            return redirect(url_for('main.editar', id=id))
        
        if usuario.foto:
            caminho_antigo = os.path.join(current_app.root_path, 'static', 'uploads', usuario.foto)
            if os.path.exists(caminho_antigo):
                os.remove(caminho_antigo)
        
        nome_arquivo = f'user_{usuario.id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.{extensao}'
        arquivo.save(os.path.join(current_app.root_path, 'static', 'uploads', nome_arquivo))
        
        usuario.foto = nome_arquivo
        db.session.commit()
        
        flash('Foto atualizada com sucesso!', 'sucesso')
    
    return redirect(url_for('main.editar', id=id))

@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'uploads'), filename)

@main.route('/usuarios/deletar/<int:id>', methods=['POST'])
@login_required
def deletar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if usuario.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário!', 'erro')
        return redirect(url_for('main.lista_usuarios'))
    
    if usuario.foto:
        caminho_foto = os.path.join(current_app.root_path, 'static', 'uploads', usuario.foto)
        if os.path.exists(caminho_foto):
            os.remove(caminho_foto)
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'sucesso')
    return redirect(url_for('main.lista_usuarios'))

@main.route('/logout')
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.login'))
