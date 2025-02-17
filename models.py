from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Empresa (Base):
    __tablename__ = "TB_EMPRESA"

    id = Column("ID_EMPRESA", Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column("NOME_EMPRESA", String)
    cnpj = Column("CNPJ", String(14), unique=True)
    endereco = Column("Endereco", String)
    email = Column("EMAIL", String)
    telefone = Column("TELEFONE", String)
    
    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa", lazy="joined", cascade="all, delete-orphan")


class ObrigacaoAcessoria (Base):
    __tablename__ = "TB_OBRIG_ACESS"

    id = Column("ID_OBRIG", Integer, primary_key=True)
    nome = Column("NOME_OBRIG", String)
    periodicidade = Column("PERIODICIDADE", String)

    empresa_id = Column("FK_EMPRESA", Integer, ForeignKey("TB_EMPRESA.ID_EMPRESA"), nullable=False)
    
    empresa = relationship("Empresa", back_populates="obrigacoes")