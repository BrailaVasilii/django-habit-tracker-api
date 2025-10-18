from django.urls import path
from .views import (
    HabitListCreateAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    PublicHabitListAPIView
)

app_name = 'habits'

urlpatterns = [
    # Listă proprii + creare
    path('', HabitListCreateAPIView.as_view(), name='habit-list-create'),

    # Habits publice
    path('public/', PublicHabitListAPIView.as_view(), name='public-habits'),

    # Detalii, update, delete
    path('<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='habit-detail'),
]