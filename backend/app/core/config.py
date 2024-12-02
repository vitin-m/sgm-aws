import secrets
from typing import Annotated

from pydantic import (
    AfterValidator,
    AnyHttpUrl,
    PostgresDsn,
    ValidationError,
    ValidationInfo,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    SettingsError,
)


def db_uri_validator(v: str, info: ValidationInfo):
    if isinstance(v, str) and v:
        return v
    values = info.data
    uri = PostgresDsn.build(
        scheme="postgresql+psycopg",
        username=values.get("POSTGRES_USER"),
        password=values.get("POSTGRES_PASSWORD"),
        host=values.get("POSTGRES_HOST"),
        port=values.get("POSTGRES_PORT"),
        path=f"{values.get('POSTGRES_DB') or ''}",
    )
    return str(uri)


class Settings(BaseSettings):
    # TODO: change .env via environment var for PROD
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    PROJECT_NAME: str

    API_PATH: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    DATABASE_URI: Annotated[str, AfterValidator(db_uri_validator)] = ""


try:
    settings = Settings()  # type: ignore
except ValidationError as e:
    raise e
except SettingsError as e:
    raise RuntimeError(".env not set propertly.") from e
