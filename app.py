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