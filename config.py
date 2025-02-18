import sys
import os
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

# Verifica se está rodando testes
if "pytest" in sys.modules:
    DATABASE_URL = DATABASE_URL_TEST  # Usa o banco de testes

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)