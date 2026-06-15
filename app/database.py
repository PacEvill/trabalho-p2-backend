from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# create_engine cria o mecanismo de conexão com o banco utilizando a URL configurada
engine = create_engine(settings.DATABASE_URL)

# SessionLocal gerencia as transações individuais (sessões) com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe base para nossos modelos do ORM SQLAlchemy
Base = declarative_base()

# Dependência do FastAPI para obter a sessão do banco e fechá-la após a requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
