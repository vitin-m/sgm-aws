from sqlmodel import SQLModel, create_engine

from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URI))


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
