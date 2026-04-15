"""
核心配置模块
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """应用配置"""
    
    PROJECT_NAME: str = "外运物流控制塔"
    PROJECT_DESCRIPTION: str = "基于数字孪生、AI预测和可视化大屏的智能物流管理平台"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/logistics_control_tower"
    DATABASE_ECHO: bool = False
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
    ]
    
    PREDICTION_SERVICE_URL: str = "http://localhost:8001"
    TIMESFM_MODEL_PATH: str = "google/timesfm-2.5-200m-pytorch"
    TIMESFM_DEVICE: str = "cpu"
    
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()