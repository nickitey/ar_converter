from dotenv import find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPIAppConfig(BaseModel):
    mount_swagger: bool
    mount_redoc: bool


class CommonAppConfig(BaseModel):
    workdir: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"), env_nested_delimiter="__"
    )

    app: FastAPIAppConfig
    common_app: CommonAppConfig
