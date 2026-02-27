from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "PriceDrop Rebuy API"
    app_env: str = "dev"
    database_url: str
    redis_url: str

    meta_verify_token: str
    meta_app_secret: str
    meta_access_token: str
    meta_phone_number_id: str
    meta_graph_version: str = "v21.0"
    telegram_bot_token: str | None = None
    telegram_webhook_secret: str | None = None

    default_check_interval_hours: int = 3
    default_min_drop_percent: float = 5.0
    alert_cooldown_hours: int = 24


settings = Settings()
