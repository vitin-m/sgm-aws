from pydantic import ValidationError
from sqlmodel import Session, select

from app.core.models import (
    UserCreate,
    User,
    UserUpdate,
    ta_emailstr,
    ta_username,
)
from app.core.security import get_password_hash, verify_password


def create_user(*, session: Session, user_create: UserCreate):
    db_obj = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, user_db: User, user_in: UserUpdate):
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if password := user_data.get("password"):
        extra_data["hashed_password"] = get_password_hash(password)
    user_db.sqlmodel_update(user_data, update=extra_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


def get_user_by_email(*, session: Session, email: str) -> User | None:
    sql = select(User).where(User.email == email)
    return session.exec(sql).first()


def get_user_by_username(*, session: Session, username: str) -> User | None:
    sql = select(User).where(User.username == username)
    return session.exec(sql).first()


def authenticate(*, session: Session, id: str, password: str) -> User | None:
    try:
        ta_emailstr.validate_python(id)
        user_db = get_user_by_email(session=session, email=id)
    except ValidationError:
        try:
            ta_username.validate_python(id)
            user_db = get_user_by_username(session=session, username=id)
        except ValidationError:
            return None

    if not user_db or not verify_password(password, user_db.hashed_password):
        return None
    return user_db
