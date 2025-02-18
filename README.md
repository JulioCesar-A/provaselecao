# Prova de Seleção de Estágio - FastAPI, Pydantic e SQLAlchemy

## Objetivo
Criar uma API utilizando **FastAPI**, **Pydantic** e **SQLAlchemy** para cadastrar empresas e gerenciar obrigações acessórias que a empresa precisa declarar para o governo.

---

## 🔧 Configuração do Ambiente

### 1️⃣ Requisitos
- **Python** (versão recomendada: 3.9 ou superior)
- **PostgreSQL**
- **Git**
- **Virtualenv** (para criação do ambiente virtual)

### 2️⃣ Instalação

#### Clone o repositório
```sh
git clone https://github.com/JulioCesar-A/provaselecao.git
cd provaselecao
```

#### Criação do ambiente virtual
```sh
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

#### Instalação das dependências
```sh
pip install -r requirements.txt
```

#### Configuração do banco de dados
Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente:
```ini
DATABASE_URL=postgresql://postgres:123456@localhost:5432/PROVA_SELECAO_DB
```

---

## 📦 Modelagem de Dados

### 1️⃣ Modelos (SQLAlchemy)
#### Empresa
| Campo    | Tipo  | Restrições |
|----------|------|-----------|
| id       | int  | Chave Primária |
| nome     | str  | Obrigatório |
| cnpj     | str  | Único e obrigatório |
| endereco | str  | Obrigatório |
| email    | str  | Obrigatório |
| telefone | str  | Obrigatório |

#### Obrigação Acessória
| Campo        | Tipo  | Restrições |
|--------------|------|-----------|
| id           | int  | Chave Primária |
| nome         | str  | Obrigatório |
| periodicidade| str  | Obrigatório |
| empresa_id   | int  | Chave Estrangeira (Empresa) |

### 2️⃣ Schemas (Pydantic)
- `EmpresaBase`,`EmpresaCreate`, `EmpresaUpdate`, `EmpresaResponse`
- `ObrigacaoAcessoriaBase`,`ObrigacaoAcessoriaCreate`, `ObrigacaoAcessoriaUpdate`, `ObrigacaoAcessoriaResponse`

---

## 🚀 Implementação de CRUD

A API segue a arquitetura RESTful e permite as seguintes operações:

### 📌 Empresa
- **Criar Empresa**: `POST /empresas`
- **Listar Empresas**: `GET /empresas`
- **Buscar Empresa por ID**: `GET /empresas/{id_empresa}`
- **Atualizar Empresa**: `PUT /empresas/{id_empresa}`
- **Deletar Empresa**: `DELETE /empresas/{id_empresa}`

### 📌 Obrigação Acessória
- **Criar Obrigação**: `POST /empresas/{id_empresa}/obrigacoes`
- **Listar Obrigações por Empresa**: `GET /empresas/{id_empresa}/obrigacoes`
- **Buscar Obrigação por ID**: `GET /empresas/{id_empresa}/obrigacoes/{id_obrigacao}`
- **Listar Obrigações por Periodicidade**: `GET /empresas/{id_empresa}/obrigacoes/{periodicidade}`
- **Atualizar Obrigação**: `PUT /empresas/{id_empresa}/obrigacoes/{id_obrigacao}`
- **Deletar Obrigação**: `DELETE /empresas/{id_empresa}/obrigacoes/{id_obrigacao}`

---

## ▶️ Como Executar a API

Após configurar o ambiente e instalar as dependências, execute o seguinte comando para iniciar a API:
```sh
uvicorn main:app --reload
```

Isso iniciará o servidor FastAPI, que poderá ser acessado em:
- **http://127.0.0.1:8000**

Para testar a API, você pode utilizar ferramentas como **Postman**, **Insomnia** ou diretamente pelo **Swagger UI** do FastAPI.

---

## 🧪 Testes Unitários

Os testes são implementados no arquivo `test_endpoints.py`, utilizando **pytest**. Para rodar os testes:
```sh
pytest
```

---

## 📜 Tratamento de Exceções

A API possui tratamento para os seguintes erros:
- **IntegrityError**: CNPJ duplicado, chave estrangeira inválida, etc.
- **HTTPException 404**: Empresa ou obrigação acessória não encontrada.
- **HTTPException 500**: Erros inesperados durante as operações no banco de dados.

---

## 📖 Documentação da API

A documentação interativa do FastAPI pode ser acessada em:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

