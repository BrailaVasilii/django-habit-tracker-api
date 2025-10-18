from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with email as primary identifier and Telegram support.

    Fields:
        email: Unique email address (used for authentication)
        telegram_chat_id: Telegram chat ID for notifications (optional)

    Authentication:
        USERNAME_FIELD: email (login cu email în loc de username)
        REQUIRED_FIELDS: username (cerut la createsuperuser)
    """

    email = models.EmailField(
        unique=True,
        verbose_name='Email Address',
        help_text='Email address used for authentication'
    )

    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID',
        help_text='Telegram chat ID for habit reminders'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self) -> str:
        """String representation: email address"""
        return self.email