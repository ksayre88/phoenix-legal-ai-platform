import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_TITLE: str = "Phoenix: Laws & Intake Engine"
    
    # Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    DEFAULT_MODEL_NAME: str = os.getenv("PHOENIX_MODEL_NAME", "qwen2.5:14b")
    
    # Email
    SMTP_HOST: str = "smtp-relay.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    INTAKE_EMAIL_FROM: str = "shawn@shawnclarklaw.com"
    
    # RAG
    CORPUS_ROOT: str = os.path.expanduser("~/legal-rag")
    RAG_DB_PATH: str = os.path.expanduser("~/legal-rag/db")
    RAG_COLLECTION_NAME: str = "legal_corpus"
    USE_RAG_BACKEND: bool = True

settings = Settings()