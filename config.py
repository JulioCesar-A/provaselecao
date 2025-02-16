import os
from sqlalchemy import create_engine, text

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

DATABASE_URL = os.getenv("DATABASE_URL")



try:
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT sqlite_version();"))
except Exception as e:
    print(f"Erro ao conectar: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
