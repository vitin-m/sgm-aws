import uuid
from datetime import datetime, timezone
from typing import Annotated, List

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    Base64Str,
    InstanceOf,
    TypeAdapter,
    EmailStr as PydanticEmailStr,
)
from pydantic.functional_validators import AfterValidator
from sqlmodel import AutoString, Field, Relationship, SQLModel

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
    profile_pic: str | None = None

class UserRegister(SQLModel):
    full_name: str = Field(max_length=255)
    username: Username
    email: EmailStr
    password: Password
    profile_pic: str | None = None

class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    username: Username | None = None
    email: EmailStr | None = None
    description: str | None = Field(default=None, max_length=2047)
    profile_pic: str | None = None

class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    profile_pic: str | None = Field(default=None, sa_type=AutoString)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    files: List["File"] = Relationship(back_populates="owner")  # Relacionamento com arquivos

class UserPublic(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    profile_pic: str | None = Field(sa_type=AutoString)

class Token(SQLModel):
    access_token: str = ""
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str | None = None
    
class File(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    filename: str = Field(max_length=255, nullable=False)
    content_type: str = Field(max_length=255, nullable=False)
    url: FileUrl = Field(nullable=False)
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    description: str | None = Field(default=None, max_length=1024)
    owner: User = Relationship(back_populates="files")
