from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RequestsConfig(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)


class PathConfig(BaseModel):
    assets: str | None = None
    constants: Path = Path("./config/constants.yml")
    messages: Path = Path("./config/messages.yml")
    commands: Path = Path("./config/commands.yml")
    requests: Path = Path("./config/requests.yml")


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        env_nested_delimiter="__",
    )

    env: Literal["dev", "prod"]

    paths: PathConfig = PathConfig()
    requests: RequestsConfig = Field(default_factory=RequestsConfig)

    tg_token: str
    tg_admins: list[int] = []

    db_name: str
    db_user: str
    db_pass: str
    db_host: str

    redis_host: str
    redis_pass: str
    redis_long_ttl: int
    redis_short_ttl: int

    # yc_folder_id: str
    # yc_api_key: str

    qn_sim_threshold: float = 0.8


config = Config()  # pyright: ignore[reportCallIssue]
