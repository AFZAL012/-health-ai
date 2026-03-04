"""Pytest configuration and fixtures."""
import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        yield db.session
