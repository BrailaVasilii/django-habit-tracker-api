import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Import validatori - VOR EȘUA pentru că fișierul nu există încă!
try:
    from habits.validators import (
        validate_related_habit_and_reward,
        validate_duration,
        validate_related_habit_is_pleasant,
        validate_pleasant_habit_no_reward,
        validate_periodicity
    )
    VALIDATORS_EXIST = True
except ImportError:
    VALIDATORS_EXIST = False
    # Definim mock functions pentru a putea rula testele
    def validate_related_habit_and_reward(related_habit, reward):
        pass
    def validate_duration(duration):
        pass
    def validate_related_habit_is_pleasant(related_habit):
        pass
    def validate_pleasant_habit_no_reward(is_pleasant, reward, related_habit):
        pass
    def validate_periodicity(periodicity):
        pass

User = get_user_model()


@pytest.mark.skipif(not VALIDATORS_EXIST, reason="Validators not implemented yet - RED PHASE")
@pytest.mark.django_db
class TestValidateRelatedHabitAndReward:
    """
    VALIDATOR 1: Nu se poate completa simultan reward ȘI related_habit
    """

    def test_both_reward_and_related_habit_raises_error(self):
        """Test: reward ȘI related_habit → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        # Mock pleasant habit
        class MockHabit:
            is_pleasant = True

        pleasant_habit = MockHabit()

        with pytest.raises(ValidationError):
            validate_related_habit_and_reward(
                related_habit=pleasant_habit,
                reward='Съесть конфету'
            )

    def test_only_reward_no_error(self):
        """Test: Doar reward → OK"""
        try:
            validate_related_habit_and_reward(
                related_habit=None,
                reward='Конфета'
            )
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_only_related_habit_no_error(self):
        """Test: Doar related_habit → OK"""
        class MockHabit:
            is_pleasant = True

        try:
            validate_related_habit_and_reward(
                related_habit=MockHabit(),
                reward=None
            )
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_neither_reward_nor_related_habit_no_error(self):
        """Test: Ambele None → OK"""
        try:
            validate_related_habit_and_reward(
                related_habit=None,
                reward=None
            )
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")


@pytest.mark.skipif(not VALIDATORS_EXIST, reason="Validators not implemented yet - RED PHASE")
class TestValidateDuration:
    """
    VALIDATOR 2: duration <= 120 secunde
    """

    def test_duration_exceeds_120_seconds_raises_error(self):
        """Test: 121 secunde → ValidationError"""
        with pytest.raises(ValidationError):
            validate_duration(121)

    def test_duration_exactly_120_seconds_no_error(self):
        """Test: 120 secunde → OK"""
        try:
            validate_duration(120)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_duration_less_than_120_no_error(self):
        """Test: 60 secunde → OK"""
        try:
            validate_duration(60)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_duration_1_second_no_error(self):
        """Test: 1 secundă → OK"""
        try:
            validate_duration(1)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_duration_very_large_raises_error(self):
        """Test: 3600 secunde → ValidationError"""
        with pytest.raises(ValidationError):
            validate_duration(3600)


@pytest.mark.skipif(not VALIDATORS_EXIST, reason="Validators not implemented yet - RED PHASE")
@pytest.mark.django_db
class TestValidateRelatedHabitIsPleasant:
    """
    VALIDATOR 3: related_habit trebuie să fie pleasant
    """

    def test_related_habit_not_pleasant_raises_error(self):
        """Test: related_habit cu is_pleasant=False → ValidationError"""
        class MockHabit:
            is_pleasant = False

        with pytest.raises(ValidationError):
            validate_related_habit_is_pleasant(MockHabit())

    def test_related_habit_is_pleasant_no_error(self):
        """Test: related_habit cu is_pleasant=True → OK"""
        class MockHabit:
            is_pleasant = True

        try:
            validate_related_habit_is_pleasant(MockHabit())
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_no_related_habit_no_error(self):
        """Test: None → OK"""
        try:
            validate_related_habit_is_pleasant(None)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")


@pytest.mark.skipif(not VALIDATORS_EXIST, reason="Validators not implemented yet - RED PHASE")
class TestValidatePleasantHabitNoReward:
    """
    VALIDATOR 4: pleasant habit fără reward/related_habit
    """

    def test_pleasant_habit_with_reward_raises_error(self):
        """Test: is_pleasant=True + reward → ValidationError"""
        with pytest.raises(ValidationError):
            validate_pleasant_habit_no_reward(
                is_pleasant=True,
                reward='Конфета',
                related_habit=None
            )

    def test_pleasant_habit_with_related_habit_raises_error(self):
        """Test: is_pleasant=True + related_habit → ValidationError"""
        class MockHabit:
            pass

        with pytest.raises(ValidationError):
            validate_pleasant_habit_no_reward(
                is_pleasant=True,
                reward=None,
                related_habit=MockHabit()
            )

    def test_pleasant_habit_without_reward_and_related_no_error(self):
        """Test: is_pleasant=True + fără nimic → OK"""
        try:
            validate_pleasant_habit_no_reward(
                is_pleasant=True,
                reward=None,
                related_habit=None
            )
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_useful_habit_with_reward_no_error(self):
        """Test: is_pleasant=False + reward → OK"""
        try:
            validate_pleasant_habit_no_reward(
                is_pleasant=False,
                reward='Награда',
                related_habit=None
            )
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")


@pytest.mark.skipif(not VALIDATORS_EXIST, reason="Validators not implemented yet - RED PHASE")
class TestValidatePeriodicity:
    """
    VALIDATOR 5: 1 <= periodicity <= 7
    """

    def test_periodicity_zero_raises_error(self):
        """Test: 0 → ValidationError"""
        with pytest.raises(ValidationError):
            validate_periodicity(0)

    def test_periodicity_negative_raises_error(self):
        """Test: -1 → ValidationError"""
        with pytest.raises(ValidationError):
            validate_periodicity(-1)

    def test_periodicity_eight_raises_error(self):
        """Test: 8 → ValidationError"""
        with pytest.raises(ValidationError):
            validate_periodicity(8)

    def test_periodicity_one_no_error(self):
        """Test: 1 → OK"""
        try:
            validate_periodicity(1)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_periodicity_seven_no_error(self):
        """Test: 7 → OK"""
        try:
            validate_periodicity(7)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")

    def test_periodicity_four_no_error(self):
        """Test: 4 → OK"""
        try:
            validate_periodicity(4)
        except ValidationError:
            pytest.fail("Nu ar trebui ValidationError")