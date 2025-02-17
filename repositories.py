from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import models, schemas
from fastapi import HTTPException

def criar_empresa(db : Session, empresa : schemas.EmpresaCreate):
    try:
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
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="CNPJ já cadastrado"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            details=f"Erro inesperado: {str(e)}"
        )

def criar_obrigacao(id : int, obrigacao : schemas.ObrigacaoAcessoriaCreate, db : Session):
    try:
        empresa_existente = db.query(models.Empresa).filter(models.Empresa.id == id).first()

        if not empresa_existente:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontrada"
            )


        nova_obrigacao = models.ObrigacaoAcessoria(
            nome = obrigacao.nome,
            periodicidade = obrigacao.periodicidade,
            empresa_id = empresa_existente.id
        )
        db.add(nova_obrigacao)
        db.commit()
        db.refresh(nova_obrigacao)
        return nova_obrigacao
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro de Integridade: Referência inválida ou dados duplicados"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        ) from e

def atualizar_dados_empresa(id: int, dados_empresa: dict, db: Session):
    try:
        empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
        
        if not empresa:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontrada"
            )

        for key, value in dados_empresa.items():
            if value is not None:
                setattr(empresa, key, value)

        db.commit()
        db.refresh(empresa)
        return empresa

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar empresa: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

def atualizar_dados_obrigacao(id_empresa: int, id_obrigacao: int, dados_obrigacao: dict, db: Session):
    try:
        obrigacao = db.query(models.ObrigacaoAcessoria).filter(
            models.ObrigacaoAcessoria.empresa_id == id_empresa,
            models.ObrigacaoAcessoria.id == id_obrigacao
        ).first()

        if not obrigacao:
            raise HTTPException(
                status_code=404,
                detail="Obrigação acessória não encontrada"
            )

        for key, value in dados_obrigacao.items():
            if value is not None:
                setattr(obrigacao, key, value)

        db.commit()
        db.refresh(obrigacao)
        return obrigacao

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar obrigação acessória: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

def listar_empresas(db : Session):
    try:
        empresas = db.query(models.Empresa).options(joinedload(models.Empresa.obrigacoes)).all()

        if not empresas:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma empresa encontrada"
            )
    
        return empresas
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar empresas: {str(e)}"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )
            
def listar_obrigacoes_por_periodicidade(id : int, periodicidade : str, db : Session):
    try:
        obrigacoes = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.empresa_id == id, models.ObrigacaoAcessoria.periodicidade == periodicidade).all()

        if not obrigacoes:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma obrigação encontrada para a periodicidade especificada"
            )

        return obrigacoes

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar obrigações: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

def buscar_empresa_por_id(id: int, db: Session):
    try:
        empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()

        if not empresa:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontrada"
            )

        return empresa

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar empresa: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

def buscar_obrigacao_por_id(id_empresa: int, id_obrigacao: int, db: Session):
    try:
        obrigacao = db.query(models.ObrigacaoAcessoria).filter(
            models.ObrigacaoAcessoria.empresa_id == id_empresa,
            models.ObrigacaoAcessoria.id == id_obrigacao
        ).first()

        if not obrigacao:
            raise HTTPException(
                status_code=404,
                detail="Obrigação não encontrada"
            )

        return obrigacao

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar obrigação: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

def deletar_empresa(id: int, db: Session):
    try:
        empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
        
        if not empresa:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontrada"
            )

        db.delete(empresa)
        db.commit()

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

def deletar_obrigacao(id_empresa: int, id_obrigacao: int, db: Session):
    try:
        empresa = db.query(models.Empresa).filter(models.Empresa.id == id_empresa)

        if not empresa:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontra"
            )
        obrigacao = db.query(models.ObrigacaoAcessoria).filter(
            models.ObrigacaoAcessoria.empresa_id == id_empresa,
            models.ObrigacaoAcessoria.id == id_obrigacao
        ).first()

        if not obrigacao:
            raise HTTPException(
                status_code=404,
                detail="Obrigação não encontrada"
            )

        db.delete(obrigacao)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar obrigação: {str(e)}"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )
