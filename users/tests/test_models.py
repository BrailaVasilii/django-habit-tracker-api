import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests pentru Custom User model"""

    def test_create_user_with_email(self):
        """Test: Creare user cu email și password"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.check_password('testpass123')
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        """Test: Creare superuser"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        assert admin.email == 'admin@example.com'
        assert admin.is_active
        assert admin.is_staff
        assert admin.is_superuser

    def test_user_email_is_unique(self):
        """Test: Email-ul trebuie să fie unic"""
        User.objects.create_user(
            email='unique@example.com',
            username='user1',
            password='pass123'
        )

        with pytest.raises(Exception):
            User.objects.create_user(
                email='unique@example.com',
                username='user2',
                password='pass456'
            )

    def test_user_str_representation(self):
        """Test: Reprezentarea string a user-ului"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        assert str(user) == 'test@example.com'

    def test_telegram_chat_id_is_optional(self):
        """Test: telegram_chat_id este opțional"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        assert user.telegram_chat_id is None

    def test_telegram_chat_id_can_be_set(self):
        """Test: telegram_chat_id poate fi setat"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            telegram_chat_id='123456789'
        )
        assert user.telegram_chat_id == '123456789'

    def test_user_email_normalization(self):
        """Test: Email-ul este normalizat (lowercase domain)"""
        user = User.objects.create_user(
            email='test@EXAMPLE.COM',
            username='testuser',
            password='pass123'
        )
        assert user.email == 'test@example.com'