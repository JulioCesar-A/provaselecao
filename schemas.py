from pydantic import BaseModel, Field
from typing import Optional, List


class ObrigacaoAcessoriaBase(BaseModel):
    nome : str
    periodicidade : str


class EmpresaBase(BaseModel):
    nome : str
    cnpj : str = Field(min_length=14, max_length=14)
    endereco : str
    email : str
    telefone : str


class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class EmpresaCreate(EmpresaBase):
    pass


class ObrigacaoAcessoriaUpdate(BaseModel):
    nome : Optional[str] = None
    periodicidade : Optional[str] = None

class EmpresaUpdate(BaseModel):
    nome : Optional[str] = None
    cnpj : Optional[str] = None
    endereco : Optional[str] = None
    email : Optional[str] = None
    telefone : Optional[str] = None



class ObrigacaoAcessoriaResponse(ObrigacaoAcessoriaBase):
    id : int
    class Config:
        from_attributes = True

class EmpresaResponse (EmpresaBase):
    id : int
    obrigacoes : List[ObrigacaoAcessoriaResponse] = []
    class Config:
        from_attributes = True