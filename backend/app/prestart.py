import logging
from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import before_log, retry, stop_after_attempt, wait_fixed

from app.core import engine
from app.core.db import init_db
from app.core import crud
from app.core.models import UserCreate, MediaFileCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Prestart>>")

@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(1),
    before=before_log(logger, logging.WARN),
)
def init(engine: Engine):
    try:
        with Session(engine) as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def user_init(engine: Engine):
    try:
        with Session(engine) as session:
            if not crud.get_user_by_email(session=session, email="admin@mail.com"):
                user_create = UserCreate(
                    full_name="admin user",
                    username="admin",
                    email="admin@mail.com",
                    password="senha123",
                )
                crud.create_user(session=session, user_create=user_create)
    except Exception as e:
        logger.error(e)
        raise e
    
def media_files_init(engine: Engine):
    try:
        with Session(engine) as session:
            if not crud.get_media_file_by_filename(session=session, filename="example.jpg"):
                media_file_create = MediaFileCreate(
                    owner_id="00000000-0000-0000-0000-000000000000",
                    filename="example.jpg",
                    content_type="image/jpeg",
                    url="https://example.com/example.jpg",
                )
                crud.create_media_file(session=session, media_file_create=media_file_create)
    except Exception as e:
        logger.error(e)
        raise e

def main():
    init(engine)
    init_db()
    user_init(engine)
    media_files_init(engine)  # Inicializar arquivos de mídia


if __name__ == "__main__":
    main()
