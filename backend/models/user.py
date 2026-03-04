"""User model for authentication and user management."""
import bcrypt
from extensions import db
from models.base import BaseModel


class User(BaseModel):
    """User model for authentication.

    Provides user authentication with email/password, role-based access control,
    and account status management.
    """

    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(50), default='patient', nullable=False)
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    profile = db.relationship(
        'UserProfile',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    analyses = db.relationship(
        'Analysis',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def set_password(self, password: str) -> None:
        """Hash and set user password using bcrypt.

        Args:
            password: Plain text password to hash
        """
        # Generate salt and hash password with cost factor 12
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def to_dict(self):
        """Convert user to dictionary, excluding sensitive fields.

        Returns:
            dict: User data without password_hash
        """
        result = super().to_dict()
        # Remove sensitive fields
        result.pop('password_hash', None)
        return result

    def __repr__(self):
        """String representation of User."""
        return f"<User {self.id}: {self.email}>"
