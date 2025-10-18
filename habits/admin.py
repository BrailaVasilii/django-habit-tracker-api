from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Admin interface pentru Habit model"""

    list_display = [
        'action',
        'user',
        'time',
        'place',
        'is_pleasant',
        'is_public',
        'periodicity',
        'duration',
        'created_at'
    ]

    list_filter = [
        'is_pleasant',
        'is_public',
        'periodicity',
        'created_at',
        'user'
    ]

    search_fields = [
        'action',
        'place',
        'user__email',
        'reward'
    ]

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Тип привычки', {
            'fields': ('is_pleasant', 'is_public')
        }),
        ('Параметры выполнения', {
            'fields': ('duration', 'periodicity')
        }),
        ('Вознаграждение', {
            'fields': ('reward', 'related_habit'),
            'description': 'Можно заполнить только одно из двух полей'
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queries with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'related_habit')