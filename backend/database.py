"""Database session management and utilities."""
from contextlib import contextmanager
from extensions import db
import logging

logger = logging.getLogger(__name__)


@contextmanager
def session_scope():
    """Provide a transactional scope for database operations.
    
    Usage:
        with session_scope() as session:
            user = User(email='test@example.com')
            session.add(user)
            # Automatically commits on success, rolls back on exception
    
    Yields:
        SQLAlchemy session
    """
    session = db.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database transaction failed: {str(e)}")
        raise
    finally:
        session.close()


def init_db(app):
    """Initialize database tables.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")


def drop_db(app):
    """Drop all database tables.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
        logger.info("Database tables dropped successfully")


def reset_db(app):
    """Reset database by dropping and recreating all tables.
    
    Args:
        app: Flask application instance
    """
    drop_db(app)
    init_db(app)
    logger.info("Database reset successfully")


def check_db_connection():
    """Check if database connection is healthy.
    
    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        # Execute a simple query to test connection
        db.session.execute(db.text('SELECT 1'))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False
