"""
Application Configuration
Uses Pydantic BaseSettings for environment variable management
Author: Sharmeen Asif
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Todo Backend API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str

    # Authentication
    better_auth_secret: str
    better_auth_url: str
    access_token_expire_minutes: int = 10080  # 7 days
    access_token_expire_minutes_remember: int = 43200  # 30 days

    # CORS
    frontend_url: str
    allowed_origins: List[str] = []

    # Security
    bcrypt_rounds: int = 12

    # Rate Limiting
    rate_limit_per_minute: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_allowed_origins(self) -> List[str]:
        """
        Get list of allowed CORS origins including Vercel preview deployments.

        Returns list containing:
        - Frontend URL
        - Localhost variants
        - Vercel preview domain pattern (if frontend_url is .vercel.app)
        """
        origins = [
            self.frontend_url,
            "http://localhost:3000",
            "http://localhost:3001",
        ]

        # Add custom allowed origins if provided
        if self.allowed_origins:
            origins.extend(self.allowed_origins)

        # Add Vercel preview deployment pattern
        if self.frontend_url.endswith(".vercel.app"):
            base_name = self.frontend_url.split("//")[1].split(".")[0]
            origins.append(f"https://{base_name}-git-*.vercel.app")

        return origins


# Global settings instance
settings = Settings()
