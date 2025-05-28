from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = '127.0.0.1'
    DB_PORT: str = '3306'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
