from datetime import datetime, timedelta, timezone
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
import jwt

from app.core.config import settings

ph = PasswordHasher()
ALGORITHM = "HS256"

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    jwt_data = {
        "exp": expire,
        "sub": str(subject)
    }
    return jwt.encode(jwt_data, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """@raises jwt.InvalidTokenError"""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    try:
        ph.verify(hashed_pwd, plain_pwd)
    except Argon2Error:
        return False
    return True

def get_password_hash(password: str) -> str:
    return ph.hash(password)
