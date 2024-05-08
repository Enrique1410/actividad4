from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresSettings(BaseSettings):
    model_config= SettingsConfigDict(env_prefix="PSQL_DB_")

    database: str
    username: str
    password: str

postgres_settings = PostgresSettings()