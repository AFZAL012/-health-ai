"""Authentication routes for user registration and login."""

from flask import request, jsonify
from marshmallow import ValidationError
import logging

from routes import api_bp
from schemas.auth_schemas import (
    RegisterRequestSchema,
    RegisterResponseSchema,
    LoginRequestSchema,
    LoginResponseSchema,
    Verify2FARequestSchema
)
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

# Initialize schemas
register_request_schema = RegisterRequestSchema()
register_response_schema = RegisterResponseSchema()

login_request_schema = LoginRequestSchema()
login_response_schema = LoginResponseSchema()

verify_2fa_request_schema = Verify2FARequestSchema()


# ================================
# REGISTER
# ================================
@api_bp.route("/auth/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = register_request_schema.load(request.get_json())

        email = data["email"]
        password = data["password"]
        profile_data = data.get("profile")
        role = data.get("role", "patient")

        user, message = AuthService.register_user(
            email=email,
            password=password,
            profile_data=profile_data,
            role=role
        )

        response_data = {
            "userId": user.id,
            "message": "Registration successful. Please check your email for the verification code."
        }

        return jsonify(register_response_schema.dump(response_data)), 201

    except ValidationError as e:
        logger.warning(f"Validation error during registration: {e.messages}")
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": e.messages
            }
        }), 400

    except ValueError as e:
        msg = str(e)

        if "already exists" in msg:
            return jsonify({
                "error": {
                    "code": "DUPLICATE_EMAIL",
                    "message": msg
                }
            }), 409

        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": msg
            }
        }), 400

    except Exception as e:
        logger.error(f"Unexpected error in register: {str(e)}", exc_info=True)

        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Unexpected server error"
            }
        }), 500


# ================================
# LOGIN
# ================================
@api_bp.route("/auth/login", methods=["POST"])
def login():
    """Authenticate user and return JWT tokens"""

    try:
        data = login_request_schema.load(request.get_json())

        email = data["email"]
        password = data["password"]

        tokens, user = AuthService.authenticate_user(email, password)

        if tokens.get("require_2fa"):
            response_data = {
                "require_2fa": True,
                "challengeId": tokens["challengeId"]
            }

        else:
            response_data = {
                "accessToken": tokens["accessToken"],
                "refreshToken": tokens["refreshToken"],
                "user": user.to_dict()
            }

        return jsonify(login_response_schema.dump(response_data)), 200

    except ValidationError as e:
        logger.warning(f"Login validation error: {e.messages}")

        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": e.messages
            }
        }), 400

    except ValueError as e:
        logger.warning(f"Authentication failed: {str(e)}")

        return jsonify({
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": str(e)
            }
        }), 401

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)

        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Unexpected server error"
            }
        }), 500


# ================================
# VERIFY 2FA
# ================================
@api_bp.route("/auth/verify-2fa", methods=["POST"])
def verify_2fa():
    """Verify OTP and return JWT tokens"""

    try:
        data = verify_2fa_request_schema.load(request.get_json())

        challenge_id = data["challengeId"]
        otp = data["otp"]

        tokens, user = AuthService.verify_otp(challenge_id, otp)

        response_data = {
            "accessToken": tokens["accessToken"],
            "refreshToken": tokens["refreshToken"],
            "user": user.to_dict()
        }

        return jsonify(login_response_schema.dump(response_data)), 200

    except ValidationError as e:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(e)
            }
        }), 400

    except ValueError as e:
        return jsonify({
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": str(e)
            }
        }), 401

    except Exception as e:
        logger.error(f"2FA verification error: {str(e)}", exc_info=True)

        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }), 500