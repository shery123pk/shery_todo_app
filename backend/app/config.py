"""
Application Configuration

Uses Pydantic BaseSettings for environment variable management.
Author: Sharmeen Asif
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Project Management System API"
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"

    # Database (Neon PostgreSQL with asyncpg)
    database_url: str

    # JWT Authentication
    jwt_secret: str = "dev-secret-key-change-in-production-min-32-chars"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days default
    access_token_expire_minutes_remember: int = 43200  # 30 days with "remember me"

    # CORS
    frontend_url: str
    allowed_origins: str = ""  # Comma-separated string

    # Email Service (SMTP)
    smtp_host: str = "smtp.sendgrid.net"
    smtp_port: int = 587
    smtp_username: str = "apikey"
    smtp_password: str = ""
    from_email: str = "noreply@example.com"

    # File Upload
    max_file_size_mb: int = 10
    upload_dir: str = "./uploads"

    # Rate Limiting
    rate_limit_per_ip: int = 100  # requests per minute per IP
    rate_limit_per_user: int = 500  # requests per minute per authenticated user

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }

    def get_allowed_origins(self) -> List[str]:
        """
        Get list of allowed CORS origins.

        Returns list containing:
        - Frontend URL
        - Localhost variants
        - Custom allowed origins from ALLOWED_ORIGINS env var
        - Vercel preview deployment pattern (if frontend_url is .vercel.app)
        """
        origins = [
            self.frontend_url,
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:3002",
            "http://localhost:3004",
        ]

        # Parse comma-separated allowed origins
        if self.allowed_origins:
            custom_origins = [
                origin.strip()
                for origin in self.allowed_origins.split(",")
                if origin.strip()
            ]
            origins.extend(custom_origins)

        # Add Vercel preview deployment pattern
        if self.frontend_url.endswith(".vercel.app"):
            base_name = self.frontend_url.split("//")[1].split(".")[0]
            origins.append(f"https://{base_name}-git-*.vercel.app")

        return list(set(origins))  # Remove duplicates

    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024


# Global settings instance
settings = Settings()
