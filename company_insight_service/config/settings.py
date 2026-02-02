import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Config
    APP_TITLE: str = "Company Intelligence API"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Deep insights into companies using LangGraph, scraping, and sentiment analysis."
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/company_insights")
    
    # RabbitMQ
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://user:password@localhost:5672/")
    RABBITMQ_QUEUE_NAME: str = "company_data_save_queue"
    
    # API Keys
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    
    # Scraping Config
    SCRAPE_TIMEOUT: int = 5
    SCRAPE_MAX_CHARS: int = 15000  # Increased limit as requested
    
    # Search Config
    DEFAULT_SEARCH_MAX_RESULTS: int = 20
    MONTHLY_EVENTS_MAX_RESULTS: int = 20
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Concurrency
    API_WORKERS: int = 8 # Default to 8 for 8-core system
    BACKGROUND_WORKERS: int = 4

    # Telegram Notification Config
    TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
