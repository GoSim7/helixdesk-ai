from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_timezone: str = "Asia/Shanghai"
    database_url: str = "sqlite:///./data/app.db"
    chatwoot_base_url: str = "http://localhost:3000"
    chatwoot_account_id: int = 1
    chatwoot_api_token: str = "replace_me"
    chatwoot_webhook_secret: str = "replace_me"
    chatwoot_timeout_seconds: float = 10.0
    chatwoot_mock_mode: bool = True
    astrbot_base_url: str = "http://localhost:6185"
    astrbot_api_key: str = "replace_me"
    astrbot_chat_path: str = "/api/bridge/chat"
    astrbot_health_path: str = "/api/bridge/health"
    astrbot_timeout_seconds: float = 20.0
    astrbot_mock_mode: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
