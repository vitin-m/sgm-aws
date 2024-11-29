import secrets
from pathlib import Path
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    AnyHttpUrl,
    Field,
    PostgresDsn,
    ValidationError,
    ValidationInfo,
)
from pydantic_settings import (
    CLI_SUPPRESS,
    BaseSettings,
    SettingsConfigDict,
    SettingsError,
)


# def env_file_validator(v: str, info: ValidationInfo):
#     return f"{info.data.get('mode')}.env"


# class LaunchSettings(BaseSettings, cli_parse_args=True):
#     mode: Literal["local", "aws"] = "local"
#     env_file: Annotated[str, AfterValidator(env_file_validator)] = Field(
#         default="", description=CLI_SUPPRESS
#     )


# launch_settings = LaunchSettings()


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
    model_config = SettingsConfigDict(env_file="local.env", extra="ignore")

    PROJECT_NAME: str

    API_PATH: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    DATABASE_URI: Annotated[str, AfterValidator(db_uri_validator)] = ""


def generate_env_file(fname: str | None = None):
    file = Path(fname or "generated.env")
    with file.open("w") as f:
        f.write(
            "\n".join(
                f"{field}="
                for (field, cfg) in Settings.model_fields.items()
                if cfg.is_required()
            )
        )

    return file


try:
    settings = Settings()  # type: ignore
except ValidationError as e:
    raise e
except SettingsError as e:
    env_file = generate_env_file()
    raise RuntimeError(
        f".env not set propertly. Generated new .env file at {env_file}"
    ) from e
