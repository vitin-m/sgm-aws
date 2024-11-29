from typing import Annotated, Generator

from app.core import engine, security, settings
from app.core.models import TokenPayload, UserInDB
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PATH}/login/access-token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> UserInDB:
    try:
        token_data = TokenPayload(**security.decode_token(token))
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user = session.get(UserInDB, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
