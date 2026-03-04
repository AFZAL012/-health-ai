"""Authentication request/response validation schemas using marshmallow."""
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class UserProfileSchema(Schema):
    """Schema for user profile data in registration."""
    age = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1, max=149, error="Age must be between 1 and 149")
    )
    gender = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )


class RegisterRequestSchema(Schema):
    """Schema for user registration request validation."""
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Invalid email format'
        }
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        error_messages={
            'required': 'Password is required',
            'invalid': 'Password must be between 8 and 128 characters'
        }
    )
    profile = fields.Nested(
        UserProfileSchema,
        required=False,
        allow_none=True
    )
    role = fields.String(
        required=False,
        validate=validate.OneOf(['patient', 'doctor', 'admin']),
        load_default='patient'
    )

    @validates('password')
    def validate_password_strength(self, value, **kwargs):
        """Validate password strength requirements.

        Password must contain:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character

        Args:
            value: Password string to validate
            **kwargs: Additional keyword arguments from marshmallow

        Raises:
            ValidationError: If password doesn't meet strength requirements
        """
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character')


class RegisterResponseSchema(Schema):
    """Schema for user registration response."""
    userId = fields.Integer(required=True)
    message = fields.String(required=True)


class LoginRequestSchema(Schema):
    """Schema for user login request validation."""
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Invalid email format'
        }
    )
    password = fields.String(
        required=True,
        error_messages={'required': 'Password is required'}
    )


class LoginResponseSchema(Schema):
    """Schema for user login response."""
    accessToken = fields.String(required=False)
    refreshToken = fields.String(required=False)
    user = fields.Dict(required=False)
    require_2fa = fields.Boolean(load_default=False)
    challengeId = fields.Integer(required=False)


class Verify2FARequestSchema(Schema):
    """Schema for 2FA verification request."""
    challengeId = fields.Integer(required=True)
    otp = fields.String(required=True, validate=validate.Length(equal=6))
