from pydantic import ValidationError
from sqlmodel import Session, select
from app.core.models import (
    UserCreate,
    User,
    UserUpdate,
    MediaFile,
    MediaFileCreate,
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

# ----- CRUD para Arquivos de Mídia -----
def create_media_file(*, session: Session, media_file_create: MediaFileCreate):
    """
    Adiciona um novo arquivo de mídia ao banco de dados.
    """
    media_file = MediaFile.model_validate(media_file_create)
    session.add(media_file)
    session.commit()
    session.refresh(media_file)
    return media_file

def get_media_files(*, session: Session, user_id: str = None):
    """
    Recupera todos os arquivos de mídia. Se `user_id` for fornecido, retorna apenas os arquivos do usuário.
    """
    sql = select(MediaFile)
    if user_id:
        sql = sql.where(MediaFile.uploaded_by == user_id)
    return session.exec(sql).all()

def get_media_file_by_id(*, session: Session, file_id: str) -> MediaFile | None:
    """
    Recupera um único arquivo de mídia pelo ID.
    """
    sql = select(MediaFile).where(MediaFile.id == file_id)
    return session.exec(sql).first()

def delete_media_file(*, session: Session, file_id: str):
    """
    Exclui um arquivo de mídia pelo ID.
    """
    media_file = get_media_file_by_id(session=session, file_id=file_id)
    if media_file:
        session.delete(media_file)
        session.commit()

def update_media_file(*, session: Session, file_id: str, media_file_update: dict):
    """
    Atualiza informações de um arquivo de mídia.
    """
    media_file = get_media_file_by_id(session=session, file_id=file_id)
    if not media_file:
        return None
    for key, value in media_file_update.items():
        setattr(media_file, key, value)
    session.add(media_file)
    session.commit()
    session.refresh(media_file)
    return media_file
