import os

# Define a variável de ambiente para usar um banco de dados SQLite de testes
# Isso deve ser feito ANTES de importar os módulos da aplicação
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# Criação do Engine SQLite exclusivo para testes
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Cria a estrutura de tabelas no banco de dados SQLite de testes.
    No final da execução de todos os testes da sessão, as tabelas são removidas.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """
    Fornece uma sessão de banco de dados isolada para cada teste.
    Utiliza transações para fazer rollback no final de cada teste, 
    garantindo que um teste não interfira no outro.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """
    Configura o TestClient do FastAPI substituindo a dependência get_db
    pelo banco de dados SQLite de testes.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
