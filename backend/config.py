"""Application configuration module."""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///medical_diagnosis.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}

    # Redis (Disabled for Windows compatibility)
    REDIS_URL = None
    CACHE_TYPE = 'SimpleCache'
    CACHE_REDIS_URL = None
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('REDIS_CACHE_TTL', 3600))

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-me')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS
    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:3000,http://localhost:5173'
    ).split(',')

    # Email
    MAIL_SERVER = os.getenv('SMTP_HOST', 'localhost')
    MAIL_PORT = int(os.getenv('SMTP_PORT', 1025))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('SMTP_USER')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('SMTP_FROM', 'noreply@medical-diagnosis.com')

    # ML Models
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/model.pkl')
    SYMPTOM_COLUMNS_PATH = os.getenv('SYMPTOM_COLUMNS_PATH', 'models/symptom_columns.pkl')
    VECTORIZER_PATH = os.getenv('VECTORIZER_PATH', 'models/vectorizer.pkl')

    # NLP
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')

    # Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_STRATEGY = 'fixed-window'

    # Session
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 1800))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # Reports
    REPORT_STORAGE_PATH = os.getenv('REPORT_STORAGE_PATH', 'reports/')
    REPORT_EXPIRY_DAYS = int(os.getenv('REPORT_EXPIRY_DAYS', 30))

    # Monitoring
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', 9090))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class StagingConfig(Config):
    """Staging configuration."""
    DEBUG = False
    LOG_LEVEL = 'INFO'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {}  # SQLite doesn't support pooling options
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = 'DEBUG'
    CACHE_TYPE = 'SimpleCache'  # Use simple cache for testing instead of Redis
    RATELIMIT_STORAGE_URL = None  # Disable rate limiting in tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
