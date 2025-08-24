import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Sat Map"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./satmap.db"
    
    # API Keys (Mock for demo)
    GOOGLE_EARTH_ENGINE_KEY: str = "mock_gee_key"
    MAPBOX_ACCESS_TOKEN: str = "mock_mapbox_token"
    OPENAI_API_KEY: str = "mock_openai_key"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "tiff", "tif"]
    UPLOAD_DIR: str = "uploads"
    
    # AI Model Settings
    TRASH_MODEL_PATH: str = "models/yolov8_trash.pt"
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # Gamification
    POINTS_PER_REPORT: int = 50
    POINTS_PER_VERIFICATION: int = 30
    POINTS_PER_SHARE: int = 10
    FALSE_REPORT_PENALTY: int = -20
    
    # Alert Thresholds
    HIGH_RISK_THRESHOLD: float = 0.8
    MEDIUM_RISK_THRESHOLD: float = 0.5
    
    # Notification Settings
    ALERT_EMAIL: str = "alerts@satmap.org"
    WEBHOOK_URL: str = "https://hooks.satmap.org/alerts"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("static/processed", exist_ok=True)