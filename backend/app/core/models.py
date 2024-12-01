import uuid
from datetime import datetime, timezone
from typing import Annotated

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    InstanceOf,
    TypeAdapter,
    EmailStr as PydanticEmailStr,
)
from pydantic.functional_validators import AfterValidator
from sqlmodel import AutoString, Field, SQLModel


def val_local_file_url(url: AnyUrl) -> AnyUrl:
    if "file" in url.scheme:
        return url
    else:
        raise ValueError("URL does not point to a local file")


def val_s3_url(url: AnyHttpUrl) -> AnyHttpUrl:
    if "s3" in url.host:
        return url
    else:
        raise ValueError("URL does not point to S3 bucket or resource")


LocalFileUrl = Annotated[AnyUrl, AfterValidator(val_local_file_url)]
S3Url = Annotated[AnyHttpUrl, AfterValidator(val_s3_url)]
FileUrl = Annotated[AnyUrl, InstanceOf[S3Url] | InstanceOf[LocalFileUrl]]

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


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    hashed_password: str
    profile_pic: FileUrl = Field(sa_type=AutoString)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Token(SQLModel):
    access_token: str = ""
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
