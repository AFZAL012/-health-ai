"""Tests for User and UserProfile models."""
import pytest
from models import User, UserProfile, db


class TestUserModel:
    """Test suite for User model."""
    
    def test_user_creation(self, app):
        """Test creating a user with valid data."""
        with app.app_context():
            user = User(
                email='test@example.com',
                role='user',
                is_active=True,
                is_verified=False
            )
            user.set_password('SecurePassword123!')
            user.save()
            
            assert user.id is not None
            assert user.email == 'test@example.com'
            assert user.role == 'user'
            assert user.is_active is True
            assert user.is_verified is False
            assert user.password_hash is not None
            assert user.created_at is not None
            assert user.updated_at is not None
    
    def test_set_password(self, app):
        """Test password hashing."""
        with app.app_context():
            user = User(email='test@example.com')
            password = 'MySecurePassword123!'
            user.set_password(password)
            
            assert user.password_hash is not None
            assert user.password_hash != password
            assert len(user.password_hash) > 0
    
    def test_check_password_valid(self, app):
        """Test password verification with correct password."""
        with app.app_context():
            user = User(email='test@example.com')
            password = 'MySecurePassword123!'
            user.set_password(password)
            
            assert user.check_password(password) is True
    
    def test_check_password_invalid(self, app):
        """Test password verification with incorrect password."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('CorrectPassword123!')
            
            assert user.check_password('WrongPassword123!') is False
    
    def test_unique_email_constraint(self, app):
        """Test that duplicate emails are rejected."""
        with app.app_context():
            user1 = User(email='duplicate@example.com')
            user1.set_password('Password123!')
            user1.save()
            
            user2 = User(email='duplicate@example.com')
            user2.set_password('Password456!')
            
            with pytest.raises(Exception):  # SQLAlchemy IntegrityError
                user2.save()
    
    def test_user_to_dict_excludes_password(self, app):
        """Test that to_dict excludes password_hash."""
        with app.app_context():
            user = User(email='test@example.com', role='user')
            user.set_password('Password123!')
            user.save()
            
            user_dict = user.to_dict()
            
            assert 'email' in user_dict
            assert 'role' in user_dict
            assert 'password_hash' not in user_dict
    
    def test_user_default_values(self, app):
        """Test default values for user fields."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            assert user.is_active is True
            assert user.is_verified is False
            assert user.role == 'user'
    
    def test_user_repr(self, app):
        """Test user string representation."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            repr_str = repr(user)
            assert 'User' in repr_str
            assert str(user.id) in repr_str
            assert user.email in repr_str


class TestUserProfileModel:
    """Test suite for UserProfile model."""
    
    def test_profile_creation(self, app):
        """Test creating a user profile with valid data."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(
                user_id=user.id,
                age=30,
                gender='male',
                medical_history=['diabetes', 'hypertension'],
                emergency_contact={'name': 'John Doe', 'phone': '555-1234'},
                language_preference='en',
                theme_preference='dark'
            )
            profile.save()
            
            assert profile.id is not None
            assert profile.user_id == user.id
            assert profile.age == 30
            assert profile.gender == 'male'
            assert profile.medical_history == ['diabetes', 'hypertension']
            assert profile.emergency_contact == {'name': 'John Doe', 'phone': '555-1234'}
            assert profile.language_preference == 'en'
            assert profile.theme_preference == 'dark'
    
    def test_profile_age_constraint_valid(self, app):
        """Test that valid age values are accepted."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=25)
            profile.save()
            
            assert profile.age == 25
    
    def test_profile_age_constraint_too_low(self, app):
        """Test that age <= 0 is rejected."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=0)
            
            with pytest.raises(Exception):  # CheckConstraint violation
                profile.save()
    
    def test_profile_age_constraint_too_high(self, app):
        """Test that age >= 150 is rejected."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=150)
            
            with pytest.raises(Exception):  # CheckConstraint violation
                profile.save()
    
    def test_profile_default_values(self, app):
        """Test default values for profile fields."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id)
            profile.save()
            
            assert profile.language_preference == 'en'
            assert profile.theme_preference == 'light'
    
    def test_profile_to_dict_json_fields(self, app):
        """Test that to_dict properly handles JSON fields."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(
                user_id=user.id,
                medical_history=['condition1'],
                emergency_contact={'name': 'Jane'}
            )
            profile.save()
            
            profile_dict = profile.to_dict()
            
            assert isinstance(profile_dict['medical_history'], list)
            assert isinstance(profile_dict['emergency_contact'], dict)
    
    def test_profile_to_dict_null_json_fields(self, app):
        """Test that to_dict handles null JSON fields."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id)
            profile.save()
            
            profile_dict = profile.to_dict()
            
            # Should default to empty list/dict
            assert profile_dict['medical_history'] == []
            assert profile_dict['emergency_contact'] == {}
    
    def test_user_profile_relationship(self, app):
        """Test one-to-one relationship between User and UserProfile."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=25)
            profile.save()
            
            # Test forward relationship
            assert profile.user.id == user.id
            assert profile.user.email == user.email
            
            # Test backward relationship
            assert user.profile.id == profile.id
            assert user.profile.age == 25
    
    def test_profile_cascade_delete(self, app):
        """Test that deleting user cascades to profile."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=25)
            profile.save()
            
            profile_id = profile.id
            user.delete()
            
            # Profile should be deleted
            deleted_profile = UserProfile.find_by_id(profile_id)
            assert deleted_profile is None
    
    def test_profile_unique_user_constraint(self, app):
        """Test that one user can only have one profile."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile1 = UserProfile(user_id=user.id, age=25)
            profile1.save()
            
            profile2 = UserProfile(user_id=user.id, age=30)
            
            with pytest.raises(Exception):  # Unique constraint violation
                profile2.save()
    
    def test_profile_repr(self, app):
        """Test profile string representation."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=25)
            profile.save()
            
            repr_str = repr(profile)
            assert 'UserProfile' in repr_str
            assert str(profile.id) in repr_str
            assert str(user.id) in repr_str


class TestUserModelEdgeCases:
    """Test edge cases for User model."""
    
    def test_password_with_special_characters(self, app):
        """Test password hashing with special characters."""
        with app.app_context():
            user = User(email='test@example.com')
            password = 'P@ssw0rd!#$%^&*()_+-=[]{}|;:,.<>?'
            user.set_password(password)
            
            assert user.check_password(password) is True
    
    def test_password_unicode_characters(self, app):
        """Test password hashing with unicode characters."""
        with app.app_context():
            user = User(email='test@example.com')
            password = 'Pässwörd123!你好'
            user.set_password(password)
            
            assert user.check_password(password) is True
    
    def test_empty_password_check(self, app):
        """Test checking empty password."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('RealPassword123!')
            
            assert user.check_password('') is False
    
    def test_user_update_method(self, app):
        """Test updating user fields."""
        with app.app_context():
            user = User(email='test@example.com', role='user')
            user.set_password('Password123!')
            user.save()
            
            user.update(role='admin', is_verified=True)
            
            assert user.role == 'admin'
            assert user.is_verified is True
    
    def test_profile_update_method(self, app):
        """Test updating profile fields."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            profile = UserProfile(user_id=user.id, age=25)
            profile.save()
            
            profile.update(age=30, gender='female')
            
            assert profile.age == 30
            assert profile.gender == 'female'
