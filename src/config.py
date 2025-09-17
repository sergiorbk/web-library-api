from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """Database configuration from environment variables"""

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "password"
    database: str = "library"
    driver: str = "postgresql+psycopg2"

    @property
    def url(self) -> str:
        """Generate database URL from components"""
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = {
        "env_prefix": "DB_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


class AppConfig(BaseSettings):
    """Application configuration from environment variables"""

    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    model_config = {
        "env_prefix": "APP_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


# Global configuration instances
db_config = DatabaseConfig()
app_config = AppConfig()


def get_database_url() -> str:
    """Get database URL from configuration"""
    return db_config.url


def get_app_config() -> AppConfig:
    """Get application configuration"""
    return app_config


def get_db_config() -> DatabaseConfig:
    """Get database configuration"""
    return db_config