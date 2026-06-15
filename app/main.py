import contextlib
from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.routers import product

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas do banco de dados na inicialização da aplicação
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Inclui o roteador do recurso de produtos
app.include_router(product.router)

@app.get("/")
def read_root():
    """
    Endpoint padrão para verificar se a API está online (Health Check).
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }
