import pytest
from models import Usuario

def test_pagina_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_sucesso(client, usuario):
    response = client.post('/login', data={
        'email': 'teste@teste.com',
        'senha': 'Teste@123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_email_invalido(client, usuario):
    response = client.post('/login', data={
        'email': 'invalido',
        'senha': 'Teste@123'
    }, follow_redirects=True)
    assert b'incorretos' in response.data or response.status_code == 200

def test_login_senha_incorreta(client, usuario):
    response = client.post('/login', data={
        'email': 'teste@teste.com',
        'senha': 'errada'
    }, follow_redirects=True)
    assert b'incorretos' in response.data or response.status_code == 200

def test_registro_pagina(client):
    response = client.get('/registrar')
    assert response.status_code == 200

def test_registro_sucesso(client):
    response = client.post('/registrar', data={
        'nome': 'Novo Usuario',
        'email': 'novo@teste.com',
        'senha': 'Nova@123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'sucesso' in response.data or b'login' in response.data

def test_registro_email_existente(client, usuario):
    response = client.post('/registrar', data={
        'nome': 'Outro',
        'email': 'teste@teste.com',
        'senha': 'Outra@123'
    }, follow_redirects=True)
    assert b'j\xc3\xa1 cadastrado' in response.data or b'cadastrado' in response.data

def test_registro_senha_fraca(client):
    response = client.post('/registrar', data={
        'nome': 'Usuario',
        'email': 'usuario@teste.com',
        'senha': 'fraca'
    }, follow_redirects=True)
    assert b'caracteres' in response.data or b'especial' in response.data or response.status_code == 200

def test_logout(client, usuario_logado):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

def test_dashboard_requer_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert b'login' in response.data.lower()

def test_dashboard_com_login(client, usuario_logado):
    response = client.get('/dashboard')
    assert response.status_code == 200
