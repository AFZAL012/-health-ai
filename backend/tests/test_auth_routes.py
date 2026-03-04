"""Tests for authentication routes."""
import pytest
import json
from models.user import User
from models.user_profile import UserProfile


class TestRegistrationEndpoint:
    """Tests for /api/v1/auth/register endpoint."""
    
    def test_register_with_valid_credentials(self, client, db_session):
        """Test user registration with valid email and password."""
        data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.get_json()
        assert 'userId' in response_data
        assert 'message' in response_data
        assert 'verification' in response_data['message'].lower()
        
        # Verify user was created in database
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
        assert user.is_active is True
        assert user.is_verified is False
        assert user.role == 'user'
    
    def test_register_with_profile_data(self, client, db_session):
        """Test user registration with profile information."""
        data = {
            'email': 'user_with_profile@example.com',
            'password': 'SecurePass123!',
            'profile': {
                'age': 30,
                'gender': 'male'
            }
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.get_json()
        assert 'userId' in response_data
        
        # Verify user and profile were created
        user = User.query.filter_by(email='user_with_profile@example.com').first()
        assert user is not None
        assert user.profile is not None
        assert user.profile.age == 30
        assert user.profile.gender == 'male'
    
    def test_register_with_duplicate_email(self, client, db_session):
        """Test registration with existing email returns 409 Conflict."""
        # Create existing user
        existing_user = User(email='existing@example.com')
        existing_user.set_password('ExistingPass123!')
        db_session.add(existing_user)
        db_session.commit()
        
        # Try to register with same email
        data = {
            'email': 'existing@example.com',
            'password': 'NewPass123!'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'DUPLICATE_EMAIL'
        assert 'already exists' in response_data['error']['message']
    
    def test_register_with_invalid_email(self, client, db_session):
        """Test registration with invalid email format returns 400."""
        data = {
            'email': 'not-an-email',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_register_with_weak_password(self, client, db_session):
        """Test registration with weak password returns 400."""
        weak_passwords = [
            'short',  # Too short
            'nouppercase123!',  # No uppercase
            'NOLOWERCASE123!',  # No lowercase
            'NoDigits!',  # No digits
            'NoSpecial123',  # No special characters
        ]
        
        for weak_password in weak_passwords:
            data = {
                'email': f'test_{weak_password}@example.com',
                'password': weak_password
            }
            
            response = client.post(
                '/api/v1/auth/register',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            assert response.status_code == 400
            response_data = response.get_json()
            assert 'error' in response_data
            assert response_data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_register_with_missing_email(self, client, db_session):
        """Test registration without email returns 400."""
        data = {
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_register_with_missing_password(self, client, db_session):
        """Test registration without password returns 400."""
        data = {
            'email': 'test@example.com'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_register_with_invalid_age(self, client, db_session):
        """Test registration with invalid age in profile returns 400."""
        data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'profile': {
                'age': 200  # Invalid age
            }
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
    
    def test_password_is_hashed(self, client, db_session):
        """Test that password is properly hashed in database."""
        data = {
            'email': 'hashtest@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        # Verify password is hashed
        user = User.query.filter_by(email='hashtest@example.com').first()
        assert user.password_hash != 'SecurePass123!'
        assert user.password_hash.startswith('$2b$')  # bcrypt hash prefix
        assert user.check_password('SecurePass123!')
        assert not user.check_password('WrongPassword')


class TestLoginEndpoint:
    """Tests for /api/v1/auth/login endpoint."""
    
    def test_login_with_valid_credentials(self, client, db_session):
        """Test login with valid credentials returns tokens."""
        # Create user
        user = User(email='logintest@example.com')
        user.set_password('SecurePass123!')
        db_session.add(user)
        db_session.commit()
        
        # Login
        data = {
            'email': 'logintest@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        response_data = response.get_json()
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert 'user' in response_data
        assert response_data['user']['email'] == 'logintest@example.com'
        assert 'password_hash' not in response_data['user']  # Sensitive data excluded
    
    def test_login_with_invalid_email(self, client, db_session):
        """Test login with non-existent email returns 401."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'AUTHENTICATION_FAILED'
    
    def test_login_with_wrong_password(self, client, db_session):
        """Test login with incorrect password returns 401."""
        # Create user
        user = User(email='wrongpass@example.com')
        user.set_password('CorrectPass123!')
        db_session.add(user)
        db_session.commit()
        
        # Try to login with wrong password
        data = {
            'email': 'wrongpass@example.com',
            'password': 'WrongPass123!'
        }
        
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        response_data = response.get_json()
        assert 'error' in response_data
        assert response_data['error']['code'] == 'AUTHENTICATION_FAILED'
    
    def test_login_with_inactive_account(self, client, db_session):
        """Test login with inactive account returns 401."""
        # Create inactive user
        user = User(email='inactive@example.com', is_active=False)
        user.set_password('SecurePass123!')
        db_session.add(user)
        db_session.commit()
        
        # Try to login
        data = {
            'email': 'inactive@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        response_data = response.get_json()
        assert 'error' in response_data
        assert 'inactive' in response_data['error']['message'].lower()
    
    def test_login_with_missing_credentials(self, client, db_session):
        """Test login without credentials returns 400."""
        # Missing password
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Missing email
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps({'password': 'SecurePass123!'}),
            content_type='application/json'
        )
        assert response.status_code == 400
