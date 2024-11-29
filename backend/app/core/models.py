import uuid
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AnyHttpUrl, TypeAdapter, EmailStr as PydanticEmailStr
from pydantic.functional_validators import AfterValidator
from sqlmodel import AutoString, Field, SQLModel


def check_s3_url(url: AnyHttpUrl) -> AnyHttpUrl:
    if "s3" in url.host:
        return url
    else:
        raise ValueError("URL does not point to S3 bucket")


S3Url = Annotated[AnyHttpUrl, AfterValidator(check_s3_url)]

Username = Annotated[str, Field(min_length=3, max_length=63)]
EmailStr = Annotated[PydanticEmailStr, Field(max_length=255)]
Password = Annotated[str, Field(min_length=8, max_length=40)]

ta_emailstr = TypeAdapter(EmailStr)
ta_username = TypeAdapter(Username)


class UserBase(SQLModel):
    full_name: str = Field(max_length=255)
    username: Username
    email: EmailStr = Field(unique=True, index=True)
    description: str | None = Field(default=None, max_length=2047)


class UserCreate(UserBase):
    password: Password


class UserRegister(SQLModel):
    full_name: str = Field(max_length=255)
    username: Username
    email: EmailStr
    password: Password


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    username: Username | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    description: str | None = Field(default=None, max_length=2047)


class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserInDB(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    hashed_password: str
    profile_pic: S3Url = Field(sa_type=AutoString)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Token(SQLModel):
    access_token: str = ""
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
