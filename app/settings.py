from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = Field(default="sqlite:///./app.db")

    # Auth (DO NOT keep default in real deployments)
    jwt_secret: str = Field(default="dev-only-change-me")
    jwt_algorithm: str = Field(default="HS256")
    jwt_exp_minutes: int = Field(default=30)

    # App behavior toggles (for detection-driven "vulnerable by design")
    verbose_auth_errors: bool = Field(default=True)
    legacy_insecure_tenant_mode: bool = Field(default=False)

    # File uploads
    upload_dir: str = Field(default="./uploads")
    max_upload_mb: int = Field(default=10)

    # Logging
    log_level: str = Field(default="INFO")

    # Optional bootstrap admin (safe pattern: set these via env in your own deploy)
    bootstrap_admin_email: str | None = Field(default=None)
    bootstrap_admin_password: str | None = Field(default=None)


settings = Settings()
