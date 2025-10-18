from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .validators import (
    validate_duration,
    validate_periodicity,
    validate_related_habit_and_reward,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit_no_reward
)


class Habit(models.Model):
    """
    Habit model - модель привычки.

    Два типа привычек:
    1. Полезная привычка (is_pleasant=False) - основное действие с вознаграждением
    2. Приятная привычка (is_pleasant=True) - способ вознаградить себя

    Attributes:
        user: Пользователь-создатель
        place: Место выполнения
        time: Время выполнения
        action: Действие
        is_pleasant: Приятная привычка (True) или полезная (False)
        related_habit: Связанная приятная привычка
        periodicity: Периодичность выполнения (1-7 дней)
        reward: Вознаграждение
        duration: Время на выполнение (макс 120 сек)
        is_public: Публичная привычка
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь',
        help_text='Создатель привычки'
    )

    place = models.CharField(
        max_length=200,
        verbose_name='Место',
        help_text='Место, где выполняется привычка'
    )

    time = models.TimeField(
        verbose_name='Время выполнения',
        help_text='Время, когда нужно выполнять привычку'
    )

    action = models.CharField(
        max_length=200,
        verbose_name='Действие',
        help_text='Действие, которое представляет собой привычка'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Является ли привычка приятной (способ вознаграждения)'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name='Связанная привычка',
        help_text='Приятная привычка, связанная с полезной'
    )

    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность (дни)',
        help_text='Периодичность выполнения (от 1 до 7 дней)'
    )

    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Вознаграждение',
        help_text='Чем вознаградить себя после выполнения'
    )

    duration = models.PositiveIntegerField(
        verbose_name='Время на выполнение (секунды)',
        help_text='Время, которое потратит пользователь (макс 120 сек)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка',
        help_text='Доступна ли привычка другим пользователям'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_public', '-created_at']),
        ]

    def __str__(self) -> str:
        """Строковое представление привычки"""
        return f'{self.action} в {self.time} ({self.place})'

    def clean(self) -> None:
        """
        Валидация модели с применением всех валидаторов.
        Вызывается перед save() через full_clean().
        """
        super().clean()

        # Validator 1: Не заполнять одновременно reward и related_habit
        validate_related_habit_and_reward(self.related_habit, self.reward)

        # Validator 2: Время выполнения <= 120 секунд
        validate_duration(self.duration)

        # Validator 3: Related habit должен быть pleasant
        if self.related_habit:
            validate_related_habit_is_pleasant(self.related_habit)

        # Validator 4: Pleasant habit без reward/related_habit
        validate_pleasant_habit_no_reward(
            self.is_pleasant,
            self.reward,
            self.related_habit
        )

        # Validator 5: Периодичность 1-7 дней
        validate_periodicity(self.periodicity)

    def save(self, *args, **kwargs) -> None:
        """
        Переопределяем save() для вызова валидации.
        """
        self.full_clean()  # Вызывает clean() и все field validators
        super().save(*args, **kwargs)