"""Tests for database configuration and base model."""
import pytest
from datetime import datetime
from app import create_app, db
from models.base import BaseModel
from database import check_db_connection, session_scope


# Create a test model for testing BaseModel functionality
class TestModel(BaseModel):
    """Test model for BaseModel functionality."""
    __tablename__ = 'test_models'
    
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, default=0)


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestDatabaseConnection:
    """Test database connection and configuration."""
    
    def test_database_connection_check(self, app):
        """Test database connection health check."""
        with app.app_context():
            assert check_db_connection() is True
    
    def test_database_uri_configured(self, app):
        """Test database URI is configured."""
        assert app.config['SQLALCHEMY_DATABASE_URI'] is not None
    
    def test_connection_pooling_configured(self, app):
        """Test connection pooling is configured."""
        engine_options = app.config['SQLALCHEMY_ENGINE_OPTIONS']
        # Skip pooling check for SQLite (testing mode)
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            assert engine_options == {}
        else:
            assert 'pool_size' in engine_options
            assert 'max_overflow' in engine_options
            assert 'pool_pre_ping' in engine_options
            assert engine_options['pool_pre_ping'] is True


class TestBaseModel:
    """Test BaseModel functionality."""
    
    def test_base_model_has_common_fields(self, app):
        """Test BaseModel has id, created_at, updated_at fields."""
        with app.app_context():
            db.create_all()
            model = TestModel(name='test')
            
            assert hasattr(model, 'id')
            assert hasattr(model, 'created_at')
            assert hasattr(model, 'updated_at')
    
    def test_base_model_save(self, app):
        """Test BaseModel save method."""
        with app.app_context():
            model = TestModel(name='test', value=42)
            saved_model = model.save()
            
            assert saved_model.id is not None
            assert saved_model.created_at is not None
            assert saved_model.updated_at is not None
    
    def test_base_model_update(self, app):
        """Test BaseModel update method."""
        with app.app_context():
            model = TestModel(name='test', value=42)
            model.save()
            
            original_updated_at = model.updated_at
            
            # Update the model
            model.update(name='updated', value=100)
            
            assert model.name == 'updated'
            assert model.value == 100
            assert model.updated_at > original_updated_at
    
    def test_base_model_delete(self, app):
        """Test BaseModel delete method."""
        with app.app_context():
            model = TestModel(name='test', value=42)
            model.save()
            model_id = model.id
            
            model.delete()
            
            # Verify model is deleted
            found = TestModel.find_by_id(model_id)
            assert found is None
    
    def test_base_model_to_dict(self, app):
        """Test BaseModel to_dict method."""
        with app.app_context():
            model = TestModel(name='test', value=42)
            model.save()
            
            result = model.to_dict()
            
            assert isinstance(result, dict)
            assert result['name'] == 'test'
            assert result['value'] == 42
            assert 'id' in result
            assert 'created_at' in result
            assert 'updated_at' in result
    
    def test_base_model_find_by_id(self, app):
        """Test BaseModel find_by_id class method."""
        with app.app_context():
            model = TestModel(name='test', value=42)
            model.save()
            
            found = TestModel.find_by_id(model.id)
            
            assert found is not None
            assert found.id == model.id
            assert found.name == 'test'
    
    def test_base_model_find_all(self, app):
        """Test BaseModel find_all class method."""
        with app.app_context():
            model1 = TestModel(name='test1', value=1)
            model2 = TestModel(name='test2', value=2)
            model1.save()
            model2.save()
            
            all_models = TestModel.find_all()
            
            assert len(all_models) == 2
            assert all_models[0].name == 'test1'
            assert all_models[1].name == 'test2'


class TestSessionManagement:
    """Test database session management."""
    
    def test_session_scope_commits_on_success(self, app):
        """Test session_scope commits transaction on success."""
        with app.app_context():
            with session_scope() as session:
                model = TestModel(name='test', value=42)
                session.add(model)
            
            # Verify model was committed
            found = TestModel.query.filter_by(name='test').first()
            assert found is not None
            assert found.value == 42
    
    def test_session_scope_rolls_back_on_error(self, app):
        """Test session_scope rolls back transaction on error."""
        with app.app_context():
            try:
                with session_scope() as session:
                    model = TestModel(name='test', value=42)
                    session.add(model)
                    # Force an error
                    raise ValueError("Test error")
            except ValueError:
                pass
            
            # Verify model was not committed
            found = TestModel.query.filter_by(name='test').first()
            assert found is None


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_endpoint(self, client):
        """Test /health endpoint returns healthy status."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'medical-diagnosis-api'
    
    def test_ready_endpoint(self, client, app):
        """Test /ready endpoint checks database connection."""
        response = client.get('/ready')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ready'
        assert 'checks' in data
        assert data['checks']['database'] is True
