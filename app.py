from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, repositories
from config import engine
from typing import List
from database import get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def home():
    return {}

# POSTs

@app.post("/empresas", response_model=schemas.EmpresaResponse, status_code=201)
def inserir_empresa(empresa : schemas.EmpresaCreate, db: Session = Depends(get_db)):
    return repositories.criar_empresa(db, empresa)

@app.post("/empresas/{id_empresa}/obrigacoes", response_model=schemas.ObrigacaoAcessoriaResponse, status_code=201)
def inserir_obrigacao(id_empresa : int, obrigacao : schemas.ObrigacaoAcessoriaCreate, db : Session = Depends(get_db)):
    return repositories.criar_obrigacao(id_empresa, obrigacao, db)

# PUTs

@app.put("/empresas/{id_empresa}", response_model=schemas.EmpresaResponse, status_code=200)
def atualizar_empresa(id_empresa : int, empresa : schemas.EmpresaUpdate, db : Session=Depends(get_db)):
    dados_empresa = empresa.model_dump(exclude_unset=True)
    return repositories.atualizar_dados_empresa(id_empresa, dados_empresa, db)

@app.put("/empresas/{id_empresa}/obrigacoes/{id_obrigacao}", response_model=schemas.ObrigacaoAcessoriaResponse, status_code=200)
def atualizar_obrigacao(id_empresa : int, id_obrigacao : int, obrigacao : schemas.ObrigacaoAcessoriaUpdate, db : Session = Depends(get_db)):
    dados_obrigacao = obrigacao.model_dump(exclude_unset=True)
    return repositories.atualizar_dados_obrigacao(id_empresa, id_obrigacao, dados_obrigacao, db)




# GETs

@app.get("/empresas/{id_empresa}/obrigacoes/{id_obrigacao}", reponse_model= schemas.ObrigacaoAcessoriaResponse, status_code=200)
def buscar_obrigacao_por_id(id_empresa : int, id_obrigacao : int, db : Session = Depends(get_db)):
    obrigacao = repositories.buscar_obrigacao_por_id(id_empresa, id_obrigacao, db)
    return obrigacao

@app.get("/empresas/{id_empresa}/obrigacoes/{periodicidade}", response_model=List[schemas.ObrigacaoAcessoriaResponse], status_code=200)
def listar_obrigacoes_por_periodicidade(id_empresa : int, periodicidade : str, db : Session = Depends(get_db)):
    return repositories.listar_obrigacoes_por_periodicidade(id_empresa, periodicidade, db)

@app.get("/empresas/{id_empresa}", response_model=schemas.EmpresaResponse, status_code=200)
def buscar_empresa_por_id(id_empresa: int, db: Session = Depends(get_db)):
    empresa = repositories.buscar_empresa_por_id(id_empresa, db)
    return empresa

@app.get("/empresas/", response_model=List[schemas.EmpresaResponse], status_code=200)
def listar_empresas(db: Session = Depends(get_db)):
    return repositories.listar_empresas(db)

# DELETEs

@app.delete("/empresas/{id_empresa}", status_code=204)
def deletar_empresa(id_empresa: int, db: Session = Depends(get_db)):
    repositories.deletar_empresa(id_empresa, db)
    return {"message" : "Removido com sucesso"}


@app.delete("/empresas/{id_empresa}/obrigacoes/{id_obrigacao}", status_code=204)
def deletar_obrigacao(id_empresa : int, id_obrigacao : int, db : Session = Depends(get_db)):
    repositories.deletar_obrigacao(id_empresa, id_obrigacao, db)
    return {"messagem" : "Removido com sucesso"}
