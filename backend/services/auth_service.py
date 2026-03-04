"""Authentication service for user registration, login, and token management."""

from typing import Optional, Dict, Any, Tuple
import logging
import random
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from flask_mail import Message

from extensions import db, mail
from models.user import User
from models.user_profile import UserProfile

logger = logging.getLogger(__name__)


class AuthService:
    """Service class for authentication operations."""

    # ==========================================
    # USER REGISTRATION
    # ==========================================
    @staticmethod
    def register_user(
        email: str,
        password: str,
        profile_data: Optional[Dict[str, Any]] = None,
        role: str = "patient",
    ) -> Tuple[User, str]:

        try:
            # Check existing user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ValueError(f"User with email {email} already exists")

            # Create user
            user = User(email=email, role=role)
            user.set_password(password)

            db.session.add(user)
            db.session.flush()  # ensure user.id available

            # Create profile if provided
            if profile_data:
                profile = UserProfile(
                    user_id=user.id,
                    age=profile_data.get("age"),
                    gender=profile_data.get("gender"),
                )
                db.session.add(profile)

            db.session.commit()

            AuthService._queue_verification_email(user)

            logger.info(f"User registered successfully: {email}")

            return user, "User registered successfully. Please verify your email."

        except IntegrityError:
            db.session.rollback()
            logger.error("Database integrity error during registration")
            raise ValueError("User already exists")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            raise

    # ==========================================
    # USER LOGIN
    # ==========================================
    @staticmethod
    def authenticate_user(email: str, password: str) -> Tuple[Dict[str, Any], User]:

        user = User.query.filter_by(email=email).first()

        if not user:
            logger.warning(f"Login attempt with unknown email: {email}")
            raise ValueError("Invalid email or password")

        if not user.check_password(password):
            logger.warning(f"Incorrect password for user: {email}")
            raise ValueError("Invalid email or password")

        if not user.is_active:
            if not user.is_verified:
                # Trigger another OTP for verification if they try to login while unverified
                AuthService.generate_otp(user)
                logger.warning(f"Unverified account login attempt: {email}. Resent OTP.")
                raise ValueError("Account not verified. A new verification code has been sent to your email.")
            else:
                logger.warning(f"Inactive account login attempt: {email}")
                raise ValueError("Account is inactive")

        # 2FA enabled
        if user.two_factor_enabled:
            otp = AuthService.generate_otp(user)

            logger.info(f"2FA OTP generated for {email}")

            return {
                "require_2fa": True,
                "challengeId": user.id
            }, user

        tokens = AuthService._generate_tokens(user)

        logger.info(f"User logged in successfully: {email}")

        return tokens, user

    # ==========================================
    # JWT TOKEN GENERATION
    # ==========================================
    @staticmethod
    def _generate_tokens(user: User) -> Dict[str, str]:
        """Generate JWT access and refresh tokens."""

        # IMPORTANT FIX: JWT subject must be string
        identity = str(user.id)

        access_token = create_access_token(
            identity=identity,
            additional_claims={
                "email": user.email,
                "role": user.role
            }
        )

        refresh_token = create_refresh_token(identity=identity)

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

    # ==========================================
    # OTP GENERATION
    # ==========================================
    @staticmethod
    def generate_otp(user: User) -> str:

        otp = "".join(str(random.randint(0, 9)) for _ in range(6))

        user.otp_code = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)

        db.session.commit()

        # Send OTP email
        try:
            msg = Message(
                "Your MediDiagnose AI Verification Code",
                recipients=[user.email],
                body=f"Your verification code is: {otp}\n\nThis code will expire in 10 minutes."
            )
            mail.send(msg)
            logger.info(f"OTP email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send OTP email: {str(e)}")
            # Log OTP for development if email fails
            logger.warning(f"DEVELOPMENT OTP FOR {user.email}: {otp}")

        return otp

    # ==========================================
    # OTP VERIFICATION
    # ==========================================
    @staticmethod
    def verify_otp(user_id: int, otp: str) -> Tuple[Dict[str, str], User]:

        user = db.session.get(User, user_id)

        if not user:
            raise ValueError("Invalid session")

        if not user.otp_code:
            raise ValueError("No verification request found")

        if user.otp_code != otp:
            logger.warning(f"Invalid OTP attempt for user {user_id}")
            raise ValueError("Invalid verification code")

        if not user.otp_expiry or user.otp_expiry < datetime.utcnow():
            logger.warning(f"Expired OTP attempt for user {user_id}")
            raise ValueError("Verification code expired")

        # clear OTP and activate user
        user.otp_code = None
        user.otp_expiry = None
        user.is_active = True
        user.is_verified = True

        db.session.commit()

        tokens = AuthService._generate_tokens(user)

        logger.info(f"2FA verification successful for user {user_id}")

        return tokens, user

    # ==========================================
    # EMAIL VERIFICATION
    # ==========================================
    @staticmethod
    def _queue_verification_email(user: User) -> None:
        """Send verification email with a code or link."""
        # For simplicity, using OTP generation for verification code
        otp = AuthService.generate_otp(user)

        try:
            msg = Message(
                "Verify your MediDiagnose AI Account",
                recipients=[user.email],
                body=f"Welcome to MediDiagnose AI!\n\nPlease verify your account using this code: {otp}"
            )
            mail.send(msg)
            logger.info(f"Verification email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            logger.warning(f"DEVELOPMENT VERIFICATION CODE FOR {user.email}: {otp}")