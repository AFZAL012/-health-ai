from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def require_role(roles):
    """
    Decorator to restrict access to specific roles via JWT.

    Args:
        roles (str | list): A single role string or a list of acceptable roles.
    """
    if isinstance(roles, str):
        roles = [roles]

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role', 'patient') # default to patient

            if user_role not in roles:
                return jsonify({
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': f'Access denied! Role {user_role} is not authorized. Required: {roles}'
                    }
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
