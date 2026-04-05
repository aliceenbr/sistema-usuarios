<<<<<<< HEAD
## Preview

### Tela inicial
![Tela inicial](print1.png)

### Dashboard
![Dashboard](print2.png)


# Sistema de Usuários

Sistema web desenvolvido com Flask.

## Funcionalidades
- Cadastro de usuários
- Login com autenticação
- CRUD completo
- Banco de dados SQLite

## Tecnologias
- Python
- Flask
- SQLite
- HTML/CSS



=======
# Sistema de Cadastro - Deploy no Render

## Passo a passo:

### 1. Crie um repositório no GitHub
1. Acesse [github.com](https://github.com)
2. Crie um novo repositório chamado `sistema-cadastro`
3. Copie o link do repositório

### 2. Envie o código para o GitHub
```bash
# Na pasta do projeto
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/sistema-cadastro.git
git branch -M main
git push -u origin main
```

### 3. Deploy no Render

1. Acesse [render.com](https://render.com)
2. Clique em **"Get Started"** → **"Web Service"**
3. Clique em **"Connect GitHub"** e autorize o acesso
4. Selecione seu repositório `sistema-cadastro`
5. Configure:
   - **Name:** `sistema-cadastro`
   - **Region:** São Paulo (ou mais próximo)
   - **Branch:** `main`
   - **Root Directory:** (deixe vazio)
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
6. Clique em **"Create Web Service"**

### 4. Aguarde o deploy
- Pode levar 1-2 minutos
- O site ficará disponível em: `https://sistema-cadastro.onrender.com`

## Recursos do Sistema

- Login e registro de usuários
- CRUD completo (Criar, Listar, Editar, Deletar)
- Upload de foto de perfil
- API REST com JSON
- Senhas criptografadas com Werkzeug
- Validação de email e senha
- Design responsivo com Bootstrap 5
- Animações suaves

## Stack Tecnológica

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Banco:** SQLite (production) / PostgreSQL (opcional)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Deploy:** Render, Gunicorn

## URLs da API

Após o deploy, você pode usar:
- `GET /api/usuarios` - Lista todos
- `GET /api/usuarios/<id>` - Busca por ID
- `POST /api/usuarios` - Cria usuário
- `PUT /api/usuarios/<id>` - Atualiza usuário
- `DELETE /api/usuarios/<id>` - Remove usuário
>>>>>>> 2190af2 (corrigindo gunicorn)
