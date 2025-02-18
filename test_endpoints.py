
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append(".")

from main import app
from database import get_db
from models import Base


DATABASE_URL_TEST = "sqlite:///PROVA_SELECAO_TEST.db"
engine = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para banco de testes
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Cria o banco de dados e suas tabelas para testes
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Apaga tabelas

# Substituir a dependência do banco nos testes
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def client():
    # Instancia o cliente de teste
    with TestClient(app) as client:
        yield client

def test_inserir_empresa(client):
    # Dados da empresa que vamos enviar para o endpoint
    empresa_data = {
        "nome": "Empresa Exemplo",
        "cnpj": "12345678000190",
        "endereco": "Rua Exemplo, 123",
        "email": "contato@empresa.com",
        "telefone": "123456789"
    }

    # Fazendo o POST para o endpoint de criar empresa
    response = client.post("/empresas", json=empresa_data)

    print(response.json())
    # Verificando se a resposta tem o código de status correto (201 - Created)
    assert response.status_code == 201


    # Verificando se a resposta contém os dados esperados
    data = response.json()
    assert data["nome"] == empresa_data["nome"]
    assert data["cnpj"] == empresa_data["cnpj"]
    assert data["endereco"] == empresa_data["endereco"]
    assert data["email"] == empresa_data["email"]
    assert data["telefone"] == empresa_data["telefone"]

def test_inserir_empresa_com_cnpj_existente(client):
    # Dados da empresa com CNPJ duplicado
    empresa_data = {
        "nome": "Empresa Exemplo Duplicada",
        "cnpj": "12345678000190",  # O mesmo CNPJ da empresa criada acima
        "endereco": "Rua Exemplo, 123",
        "email": "contato@empresa.com",
        "telefone": "123456789"
    }

    # Fazendo o POST para o endpoint de criar empresa
    response = client.post("/empresas", json=empresa_data)

    print(response.json())
    # Verificando se a resposta tem o código de status 400 (erro de integridade)
    assert response.status_code == 400
    assert response.json() == {"detail": "CNPJ já cadastrado"}

def test_listar_empresas(client):
    # Fazendo o GET para listar as empresas
    response = client.get("/empresas/")

    print(response.json())
    # Verificando se o status code da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificando se a resposta é uma lista
    data = response.json()
    assert isinstance(data, list)

def test_buscar_empresa_por_id(client):
    # Criar a empresa primeiro
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678000191",
        "endereco": "Rua Teste, 456",
        "email": "contato@teste.com",
        "telefone": "987654321"
    }
    post_response = client.post("/empresas", json=empresa_data)
    empresa_id = post_response.json()["id"]  # Pegando o ID da empresa criada

    print(post_response.json())
    # Fazendo o GET para buscar a empresa pelo ID
    response = client.get(f"/empresas/{empresa_id}")

    print(response.json())
    # Verificando se a resposta tem o código de status 200 (OK)
    assert response.status_code == 200

    # Verificando se a resposta contém os dados da empresa correta
    data = response.json()
    assert data["id"] == empresa_id
    assert data["nome"] == empresa_data["nome"]

def test_buscar_empresa_por_id_inexistente(client):
    # Fazendo o GET para buscar uma empresa inexistente
    response = client.get("/empresas/100")
    print(response.json())

    # Verificando se o status code é 404 (não encontrado)
    assert response.status_code == 404
    assert response.json() == {"detail": "Empresa não encontrada"}
