from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SATUSEHAT_BASE_URL: str = ""
    SATUSEHAT_TOKEN_URL: str = ""

    SATUSEHAT_CLIENT_ID: str = ""
    SATUSEHAT_CLIENT_SECRET: str = ""

    SATUSEHAT_ORG_ID: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()