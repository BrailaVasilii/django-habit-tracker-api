from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission: utilizatorul poate accesa doar propriile habits.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifică dacă user-ul este owner-ul habit-ului.

        Args:
            request: HTTP request object
            view: View object
            obj: Habit object

        Returns:
            bool: True dacă user este owner, False altfel
        """
        return obj.user == request.user