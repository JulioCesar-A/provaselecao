from sqlalchemy.orm import Session
import models, schemas


def criar_empresa(db : Session, empresa : schemas.EmpresaCreate):
    nova_empresa = models.Empresa(
        nome = empresa.nome,
        cnpj = empresa.cnpj,
        endereco = empresa.endereco,
        email = empresa.email,
        telefone = empresa.telefone
    )
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa

def criar_obrigacao(id : int, obrigacao : schemas.ObrigacaoAcessoriaCreate, db : Session):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()


    nova_obrigacao = models.ObrigacaoAcessoria(
        nome = obrigacao.nome,
        periodicidade = obrigacao.periodicidade,
        empresa_id = empresa.id
    )
    db.add(nova_obrigacao)
    db.commit()
    db.refresh(nova_obrigacao)
    return nova_obrigacao

