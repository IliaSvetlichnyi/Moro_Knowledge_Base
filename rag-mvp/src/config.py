from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    PGHOST: str = "localhost"
    PGPORT: int = 5432
    PGDATABASE: str = "rag"
    PGUSER: str = "postgres"
    PGPASSWORD: str = "postgres"

    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api"
    OPENROUTER_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"

    # Models
    EMBED_MODEL: str = "BAAI/bge-small-en"
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    RERANKER_ENABLED: bool = True

    # Retrieval knobs
    DENSE_TOP_K: int = 20
    BM25_TOP_K: int = 20
    RERANK_TOP_K: int = 5
    CHUNK_TOKENS: int = 250
    CHUNK_OVERLAP: float = 0.15

    MAX_NEW_TOKENS: int = 300
    TEMPERATURE: float = 0.2

    class Config:
        env_file = ".env"


settings = Settings()

