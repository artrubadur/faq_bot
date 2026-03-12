from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RequestsConfig(BaseModel):
    model_config = ConfigDict(extra="allow")


class PathConfig(BaseModel):
    logging: Path = Path("./config/logging.yml")
    constants: Path = Path("./config/constants.yml")
    messages: Path = Path("./config/messages.yml")
    commands: Path = Path("./config/commands.yml")
    requests: Path = Path("./config/requests.yml")


class BotConfig(BaseModel):
    token: str
    admins: list = Field(default_factory=list)


class DBConfig(BaseModel):
    name: str
    user: str
    password: str
    host: str


class RedisConfig(BaseModel):
    host: str
    password: str
    long_ttl: int
    short_ttl: int


class QuestionsConfig(BaseModel):
    sim_threshold: float = Field(default=0.8, ge=0.0, le=1.0)


class RateLimitConfig(BaseModel):
    enabled: bool = True
    max_requests: int = Field(default=5, ge=1)
    window: int = Field(default=10, ge=1)
    skip_admin: bool = True


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        env_nested_delimiter="__",
    )

    paths: PathConfig = PathConfig()
    requests: RequestsConfig
    bot: BotConfig
    db: DBConfig
    redis: RedisConfig
    questions: QuestionsConfig = Field(default_factory=QuestionsConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)


config = Config()  # pyright: ignore[reportCallIssue]
