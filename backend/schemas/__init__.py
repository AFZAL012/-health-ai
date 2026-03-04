"""Schemas package initialization."""
from schemas.auth_schemas import (
    RegisterRequestSchema,
    RegisterResponseSchema,
    LoginRequestSchema,
    LoginResponseSchema
)

__all__ = [
    'RegisterRequestSchema',
    'RegisterResponseSchema',
    'LoginRequestSchema',
    'LoginResponseSchema'
]
