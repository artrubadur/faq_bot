from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_token: str
    database_url: str


config = Config()  # pyright: ignore[reportCallIssue]
