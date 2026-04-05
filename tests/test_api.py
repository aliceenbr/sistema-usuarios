import pytest
import json

def test_api_listar_vazia(client):
    response = client.get('/api/usuarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_api_criar_usuario(client):
    response = client.post('/api/usuarios', 
        data=json.dumps({
            'nome': 'API Usuario',
            'email': 'api@teste.com',
            'senha': 'Api@123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['nome'] == 'API Usuario'

def test_api_criar_email_invalido(client):
    response = client.post('/api/usuarios',
        data=json.dumps({
            'nome': 'Teste',
            'email': 'invalido',
            'senha': 'Teste@123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_api_buscar(client, usuario):
    response = client.get('/api/usuarios/buscar?q=Teste')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_api_detalhes(client, usuario):
    response = client.get(f'/api/usuarios/{usuario}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'teste@teste.com'

def test_api_detalhes_nao_existe(client):
    response = client.get('/api/usuarios/9999')
    assert response.status_code == 404
