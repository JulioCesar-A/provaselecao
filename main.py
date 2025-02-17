from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
import models, schemas, repositories
from config import engine
from typing import List
from database import get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = "Gestão de Empresas API",
    description = "API para gerenciar empresas e suas obrigações fiscais"
)

@app.get("/")
def home():
    return {}

@app.post("/empresas", response_model=schemas.EmpresaResponse, status_code=201, summary="Inserir Empresa", description="Insere os dados de uma empresa")
def inserir_empresa(empresa : schemas.EmpresaCreate, db: Session = Depends(get_db)):
    try:
        return repositories.criar_empresa(db, empresa)
        
    except HTTPException as error:
        raise error
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade: CNPJ já cadastrado ou dados duplicados."
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )
    
@app.post("/empresas/{id_empresa}/obrigacoes", response_model=schemas.ObrigacaoAcessoriaResponse, status_code=201, summary="Inserir Obrigação", description="Insere os dados de uma obrigação acessória de uma empresa especificada pelo ID")
def inserir_obrigacao(id_empresa : int, obrigacao : schemas.ObrigacaoAcessoriaCreate, db : Session = Depends(get_db)):
    try:
        return repositories.criar_obrigacao(id_empresa, obrigacao, db)

    except HTTPException as error:
        raise error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao tentar criar a obrigação acessória: {str(e)}"
        )

@app.put("/empresas/{id_empresa}", response_model=schemas.EmpresaResponse, status_code=200, summary="Atualizar Empresa", description="Atualiza os dados de uma empresa especificada pelo ID")
def atualizar_empresa(id_empresa : int, empresa : schemas.EmpresaUpdate, db : Session=Depends(get_db)):
    try:
        dados_empresa = empresa.model_dump(exclude_unset=True)
        return repositories.atualizar_dados_empresa(id_empresa, dados_empresa, db)

    except HTTPException as error:
        raise error
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao atualizar empresa: {str(e)}"
        )

@app.put("/empresas/{id_empresa}/obrigacoes/{id_obrigacao}", response_model=schemas.ObrigacaoAcessoriaResponse, status_code=200, summary="Atualizar Obrigação", description="Atualiza os dados de uma obrigação acessória de uma empresa")
def atualizar_obrigacao(id_empresa : int, id_obrigacao : int, obrigacao : schemas.ObrigacaoAcessoriaUpdate, db : Session = Depends(get_db)):
    try:
        dados_obrigacao = obrigacao.model_dump(exclude_unset=True)
        return repositories.atualizar_dados_obrigacao(id_empresa, id_obrigacao, dados_obrigacao, db)

    except HTTPException as error:
        raise error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao atualizar obrigação acessória: {str(e)}"
        )

@app.get("/empresas/{id_empresa}/obrigacoes/{id_obrigacao : int}", response_model= schemas.ObrigacaoAcessoriaResponse, status_code=200, summary="Buscar Obrigação por ID", description="Recupera uma obrigação acessória específica de uma empresa pelo seu ID")
def buscar_obrigacao_por_id(id_empresa: int, id_obrigacao: int, db: Session = Depends(get_db)):
    try:
        return repositories.buscar_obrigacao_por_id(id_empresa, id_obrigacao, db)

    except HTTPException as error:
        raise error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar a obrigação: {str(e)}"
        )

@app.get("/empresas/{id_empresa}/obrigacoes/{periodicidade : str}", response_model=List[schemas.ObrigacaoAcessoriaResponse], status_code=200, summary= "Listar Obrigações Acessórias por Periodicidade", description= "Recupera uma lista com todas as obrigações acessórias de uma empresa com a mesma periodicidade")
def listar_obrigacoes_por_periodicidade(id_empresa : int, periodicidade : str, db : Session = Depends(get_db)):
    try:
        return repositories.listar_obrigacoes_por_periodicidade(id_empresa, periodicidade.capitalize(), db)

    except HTTPException as error:
        raise error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar obrigações por periodicidade: {str(e)}"
        )

@app.get("/empresas/{id_empresa}", response_model=schemas.EmpresaResponse, status_code=200, summary="Buscar Empresa por ID", description="Recupera uma empresa pelo seu ID")
def buscar_empresa_por_id(id_empresa: int, db: Session = Depends(get_db)):
    try:
        empresa = repositories.buscar_empresa_por_id(id_empresa, db)
        return empresa
    except HTTPException as error:
        raise error
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar obrigações por periodicidade: {str(e)}"
        )

@app.get("/empresas/", response_model=List[schemas.EmpresaResponse], status_code=200, summary="Listar Empresas", description="Recupera uma lista com todas as empresas e suas obrigações")
def listar_empresas(db: Session = Depends(get_db)):
    try:
        empresas = repositories.listar_empresas(db)
        return empresas
    
    except HTTPException as error:
        raise error
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar obrigações por periodicidade: {str(e)}"
        )

@app.delete("/empresas/{id_empresa}", status_code=204, summary="Deletar Empresa", description="Deleta uma empresa e suas obrigações acessórias pelo ID da empresa")
def deletar_empresa(id_empresa: int, db: Session = Depends(get_db)):
    try:
        repositories.deletar_empresa(id_empresa, db)
        return {"message" : "Removido com sucesso"}
    except HTTPException as error:
        raise error
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar empresa: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

@app.delete("/empresas/{id_empresa}/obrigacoes/{id_obrigacao}", status_code=204, summary="Deletar Obrigação Acessória", description="Deleta uma obrigação acessória de uma empresa pelo ID da obrigação")
def deletar_obrigacao(id_empresa : int, id_obrigacao : int, db : Session = Depends(get_db)):
    try:
        repositories.deletar_obrigacao(id_empresa, id_obrigacao, db)
        return {"message" : "Removido com sucesso"}

    except HTTPException as error:
        raise error
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar obrigação acessória: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )