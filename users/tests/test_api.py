import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Tests pentru user registration endpoint"""

    def test_register_user_success(self):
        """Test: Înregistrare user cu date valide"""
        client = APIClient()
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }

        response = client.post('/api/users/register/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'newuser@example.com'
        assert 'password' not in response.data
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_register_user_password_mismatch(self):
        """Test: Înregistrare eșuează la parole diferite"""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!'
        }

        response = client.post('/api/users/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_duplicate_email(self):
        """Test: Înregistrare eșuează la email duplicat"""
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='pass123'
        )

        client = APIClient()
        data = {
            'email': 'existing@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }

        response = client.post('/api/users/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestJWTAuthentication:
    """Tests pentru JWT authentication"""

    def test_obtain_token_success(self):
        """Test: Obținere token cu credențiale valide"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        response = client.post('/api/users/token/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_obtain_token_invalid_credentials(self):
        """Test: Obținere token eșuează cu credențiale invalide"""
        client = APIClient()
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }

        response = client.post('/api/users/token/', data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED