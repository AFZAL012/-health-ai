from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()
from flask import request as flask_request

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "500 per hour"]
)

@limiter.request_filter
def skip_options():
    return flask_request.method == 'OPTIONS'
