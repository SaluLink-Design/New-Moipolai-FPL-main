from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        protected_namespaces=(),
        env_file=".env",
        case_sensitive=False
    )
    
    # Environment
    env: str = "development"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    @property
    def port(self) -> int:
        """Get port from environment, Railway sets PORT automatically."""
        import os
        return int(os.getenv("PORT", self.api_port))
    
    # Database
    database_url: str = "sqlite:///./fpl_ai.db"
    supabase_url: str = ""
    supabase_anon_key: str = ""
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # FPL API
    fpl_api_base_url: str = "https://fantasy.premierleague.com/api"
    fpl_cache_ttl: int = 3600  # 1 hour
    fpl_deadline_cache_ttl: int = 300  # 5 minutes
    
    # ML Models
    model_path: str = "./models"
    model_version: str = "v1"
    retrain_schedule: str = "0 2 * * 1"  # Cron expression
    
    # OCR
    ocr_engine: str = "easyocr"  # tesseract or easyocr
    ocr_languages: str = "en"
    ocr_confidence_threshold: float = 0.6
    
    # Fuzzy Matching
    fuzzy_match_threshold: int = 80
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000,https://*.fly.dev"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Monitoring
    sentry_dsn: str = ""
    mlflow_tracking_uri: str = "./mlruns"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"


# Global settings instance
settings = Settings()
