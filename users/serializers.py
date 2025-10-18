from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer principal pentru User model.
    Folosit pentru operațiuni CRUD pe users.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'password_confirm',
            'telegram_chat_id',
            'first_name',
            'last_name',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def validate(self, attrs):
        """Validare: password și password_confirm trebuie să coincidă"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        """Creare user cu password hash-uit"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Serializer pentru informații publice despre user.
    Fără date sensibile (password, email complet, etc).
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = fields