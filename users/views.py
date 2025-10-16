from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Endpoint pentru înregistrare user nou.

    POST /api/users/register/

    Permissions: AllowAny (nu trebuie să fii autentificat)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Creare user și returnare răspuns"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'message': 'User created successfully'
            },
            status=status.HTTP_201_CREATED
        )