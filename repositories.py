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


def atualizar_dados_empresa(id : int, dados_empresa : dict, db : Session):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if empresa:
        for key, value in dados_empresa.items():
            if value is not None:
                setattr(empresa, key, value)
    db.commit()
    db.refresh(empresa)
    return empresa

def atualizar_dados_obrigacao(id_empresa : int, id_obrigacao : int, dados_obrigacao : dict, db : Session):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.empresa_id == id_empresa, models.ObrigacaoAcessoria.id == id_obrigacao).first()
    if obrigacao:
        for key, value in dados_obrigacao.items():
            if value is not None:
                setattr(obrigacao, key, value)
    db.commit()
    db.refresh(obrigacao)
    return obrigacao