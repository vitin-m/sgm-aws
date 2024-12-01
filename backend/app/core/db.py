from sqlmodel import create_engine

from app.core import settings
from app.core.models import SQLModel

engine = create_engine(str(settings.DATABASE_URI))


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
