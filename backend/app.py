"""Main Flask application factory."""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

from config import config

from extensions import db, jwt, cache, limiter, mail


def create_app(config_name=None):
    """Create and configure the Flask application.

    Args:
        config_name: Configuration name (development, staging, production)

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Configure logging
    setup_logging(app)

    # Register blueprints
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Basic health check endpoint."""
        return {'status': 'healthy', 'service': 'medical-diagnosis-api'}, 200

    @app.route('/ready')
    def readiness_check():
        """Readiness check endpoint."""
        from database import check_db_connection

        checks = {
            'database': check_db_connection(),
            'service': 'medical-diagnosis-api'
        }

        # Return 503 if any check fails
        if not all([checks['database']]):
            return {'status': 'not_ready', 'checks': checks}, 503

        return {'status': 'ready', 'checks': checks}, 200

    return app


def setup_logging(app):
    """Configure application logging.

    Args:
        app: Flask application instance
    """
    log_level = getattr(logging, app.config['LOG_LEVEL'])

    # Create logs directory if it doesn't exist
    log_file = app.config['LOG_FILE']
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Configure app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # Suppress werkzeug logs in production
    if not app.config['DEBUG']:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
