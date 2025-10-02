from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.config import settings


def get_engine() -> Engine:
    url = f"postgresql+psycopg2://{settings.PGUSER}:{settings.PGPASSWORD}@{settings.PGHOST}:{settings.PGPORT}/{settings.PGDATABASE}"
    engine = create_engine(url, pool_pre_ping=True)
    return engine

