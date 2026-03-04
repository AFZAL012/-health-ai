"""Routes package initialization."""
from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from routes import auth
from routes.predict import predict_bp

api_bp.register_blueprint(predict_bp, url_prefix='/predict')

__all__ = ['api_bp']
