from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import (
    HabitSerializer,
    PublicHabitSerializer,
    HabitListSerializer
)
from .permissions import IsOwner
from .pagination import HabitPagination


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint: Listă habits proprii + Creare habit nou.

    GET /api/habits/ - listă propriile habits (paginate, 5/page)
    POST /api/habits/ - creare habit nou

    Permissions: IsAuthenticated
    Pagination: 5 items per page
    """

    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_serializer_class(self):
        """Returnează serializer diferit pentru list vs create"""
        if self.request.method == 'GET':
            return HabitListSerializer
        return HabitSerializer

    def get_queryset(self):
        """Returnează doar habits-urile user-ului autentificat"""
        return Habit.objects.filter(
            user=self.request.user
        ).select_related('user', 'related_habit').order_by('-created_at')

    def perform_create(self, serializer):
        """Setează user-ul curent ca owner la creare"""
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint: Detalii, actualizare, ștergere habit.

    GET /api/habits/{id}/ - detalii habit
    PUT/PATCH /api/habits/{id}/ - actualizare habit
    DELETE /api/habits/{id}/ - ștergere habit

    Permissions: IsAuthenticated + IsOwner
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Returnează doar habits-urile user-ului autentificat"""
        return Habit.objects.filter(
            user=self.request.user
        ).select_related('user', 'related_habit')


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Endpoint: Listă habits publice.

    GET /api/habits/public/ - toate habits publice (read-only)

    Permissions: IsAuthenticated
    Pagination: 5 items per page
    """

    serializer_class = PublicHabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Returnează doar habits publice"""
        return Habit.objects.filter(
            is_public=True
        ).select_related('user').order_by('-created_at')