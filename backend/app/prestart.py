import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import before_log, retry, stop_after_attempt, wait_fixed

from app.core import engine
from app.core.db import init_db

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


def main():
    init(engine)
    init_db()


if __name__ == "__main__":
    main()
