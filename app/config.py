from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/trabalhop2"
    PROJECT_NAME: str = "API de Gerenciamento de Produtos"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
