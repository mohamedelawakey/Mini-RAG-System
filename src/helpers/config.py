from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App metadata
    APP_NAME: str
    APP_VERSION: str

    # External services
    OPENAI_API_KEY: str

    # File upload configs
    FILE_ALLOWED_TYPES: list[str]
    FILE_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    # Load values from .env file
    model_config = SettingsConfigDict(
        env_file=".env"
    )


def get_settings():
    # FastAPI dependency to get settings
    return Settings()
