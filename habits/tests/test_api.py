import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabitCreation:
    """Tests pentru creare habits"""

    def test_create_habit_success(self):
        """Test: Creare habit cu date valide"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'place': 'Парк',
            'time': '07:00:00',
            'action': 'Пробежка 2 км',
            'is_pleasant': False,
            'duration': 120,
            'periodicity': 1,
            'reward': 'Протеиновый коктейль'
        }

        response = client.post('/api/habits/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['action'] == 'Пробежка 2 км'
        assert Habit.objects.count() == 1

    def test_create_habit_duration_over_120_fails(self):
        """Test: Creare habit cu duration > 120 eșuează"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'place': 'Офис',
            'time': '14:00:00',
            'action': 'Работа',
            'is_pleasant': False,
            'duration': 150,  # > 120
            'reward': 'Перерыв'
        }

        response = client.post('/api/habits/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_habit_unauthenticated_fails(self):
        """Test: User neautentificat nu poate crea habit"""
        client = APIClient()

        data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'duration': 60,
            'reward': 'Бодрость'
        }

        response = client.post('/api/habits/', data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestHabitList:
    """Tests pentru listă habits"""

    def test_list_own_habits(self):
        """Test: User vede doar propriile habits"""
        user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='pass123'
        )
        user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='pass123'
        )

        # Habits pentru user1
        Habit.objects.create(
            user=user1,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        # Habits pentru user2
        Habit.objects.create(
            user=user2,
            place='Парк',
            time='07:00:00',
            action='Пробежка',
            is_pleasant=False,
            duration=120,
            reward='Протеин'
        )

        client = APIClient()
        client.force_authenticate(user=user1)

        response = client.get('/api/habits/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['action'] == 'Зарядка'

    def test_list_habits_pagination(self):
        """Test: Habits sunt paginate la 5 per pagină"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        # Creăm 7 habits
        for i in range(7):
            Habit.objects.create(
                user=user,
                place=f'Место {i}',
                time='08:00:00',
                action=f'Действие {i}',
                is_pleasant=False,
                duration=60,
                reward='Награда'
            )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/api/habits/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5  # Max 5 per page
        assert response.data['count'] == 7


@pytest.mark.django_db
class TestHabitDetail:
    """Tests pentru detalii habit"""

    def test_retrieve_own_habit(self):
        """Test: User poate vedea propriul habit"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f'/api/habits/{habit.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['action'] == 'Зарядка'

    def test_retrieve_other_user_habit_fails(self):
        """Test: User NU poate vedea habit-ul altui user"""
        user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='pass123'
        )
        user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user1,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        client = APIClient()
        client.force_authenticate(user=user2)

        response = client.get(f'/api/habits/{habit.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestHabitUpdate:
    """Tests pentru actualizare habit"""

    def test_update_own_habit(self):
        """Test: User poate actualiza propriul habit"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        data = {'action': 'Пробежка'}
        response = client.patch(f'/api/habits/{habit.id}/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['action'] == 'Пробежка'


@pytest.mark.django_db
class TestHabitDelete:
    """Tests pentru ștergere habit"""

    def test_delete_own_habit(self):
        """Test: User poate șterge propriul habit"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(f'/api/habits/{habit.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Habit.objects.filter(id=habit.id).exists()


@pytest.mark.django_db
class TestPublicHabits:
    """Tests pentru habits publice"""

    def test_list_public_habits(self):
        """Test: Listă habits publice"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        # Habit public
        Habit.objects.create(
            user=user,
            place='Парк',
            time='07:00:00',
            action='Пробежка',
            is_pleasant=False,
            duration=120,
            reward='Протеин',
            is_public=True
        )

        # Habit privat
        Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе',
            is_public=False
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/api/habits/public/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['action'] == 'Пробежка'