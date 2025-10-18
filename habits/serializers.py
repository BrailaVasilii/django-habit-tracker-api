from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Serializer principal pentru Habit.
    Folosit pentru CRUD operations.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'duration',
            'is_public',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validare la nivel de serializer.
        Model.clean() va fi apelat automat la save().
        """
        # Creăm instanță temporară pentru validare
        instance = self.instance if self.instance else Habit(**data)

        # Actualizăm cu noile date
        for key, value in data.items():
            setattr(instance, key, value)

        # Apelăm clean() pentru validare
        instance.clean()

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    """
    Serializer pentru habits publice.
    Read-only, arată doar informații publice.
    """

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id',
            'user_email',
            'place',
            'time',
            'action',
            'is_pleasant',
            'periodicity',
            'duration',
            'created_at'
        ]
        read_only_fields = fields


class HabitListSerializer(serializers.ModelSerializer):
    """
    Serializer pentru listă de habits (optimizat, mai puține câmpuri).
    """

    class Meta:
        model = Habit
        fields = [
            'id',
            'action',
            'place',
            'time',
            'is_pleasant',
            'is_public',
            'periodicity',
            'duration',
            'created_at'
        ]
        read_only_fields = fields