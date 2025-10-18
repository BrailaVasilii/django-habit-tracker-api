"""
Validators pentru Habit model.
Validează regulile de business conform cerințelor proiectului.
"""
from django.core.exceptions import ValidationError


def validate_related_habit_and_reward(related_habit, reward) -> None:
    """
    Validator 1: Исключить одновременный выбор связанной привычки и вознаграждения.

    Regula: Nu se poate completa simultan reward ȘI related_habit.
    Trebuie să fie completat DOAR unul din cele două sau niciunul.

    Args:
        related_habit: Obiect Habit sau None
        reward: String sau None

    Raises:
        ValidationError: Dacă ambele sunt completate

    Examples:
        >>> validate_related_habit_and_reward(habit_obj, "Награда")  # ValidationError
        >>> validate_related_habit_and_reward(habit_obj, None)       # OK
        >>> validate_related_habit_and_reward(None, "Награда")       # OK
        >>> validate_related_habit_and_reward(None, None)            # OK
    """
    if related_habit and reward:
        raise ValidationError(
            'Нельзя одновременно указывать связанную привычку и вознаграждение. '
            'Выберите что-то одно.'
        )


def validate_duration(duration: int) -> None:
    """
    Validator 2: Время выполнения должно быть не больше 120 секунд.

    Regula: duration <= 120 secunde

    Args:
        duration: Timpul de execuție în secunde

    Raises:
        ValidationError: Dacă duration > 120

    Examples:
        >>> validate_duration(120)  # OK
        >>> validate_duration(60)   # OK
        >>> validate_duration(121)  # ValidationError
    """
    if duration > 120:
        raise ValidationError(
            f'Время выполнения не должно превышать 120 секунд. '
            f'Указано: {duration} секунд.'
        )


def validate_related_habit_is_pleasant(related_habit) -> None:
    """
    Validator 3: В связанные привычки могут попадать только привычки
    с признаком приятной привычки.

    Regula: Dacă există related_habit, trebuie să aibă is_pleasant=True

    Args:
        related_habit: Obiect Habit sau None

    Raises:
        ValidationError: Dacă related_habit există și is_pleasant=False

    Examples:
        >>> validate_related_habit_is_pleasant(pleasant_habit)  # OK (is_pleasant=True)
        >>> validate_related_habit_is_pleasant(useful_habit)    # ValidationError
        >>> validate_related_habit_is_pleasant(None)            # OK
    """
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            'В связанные привычки можно выбирать только приятные привычки.'
        )


def validate_pleasant_habit_no_reward(is_pleasant: bool, reward, related_habit) -> None:
    """
    Validator 4: У приятной привычки не может быть вознаграждения
    или связанной привычки.

    Regula: Dacă is_pleasant=True → reward=None ȘI related_habit=None

    Args:
        is_pleasant: Boolean flag - este privinică plăcută?
        reward: String sau None
        related_habit: Obiect Habit sau None

    Raises:
        ValidationError: Dacă is_pleasant=True și există reward sau related_habit

    Examples:
        >>> validate_pleasant_habit_no_reward(True, None, None)      # OK
        >>> validate_pleasant_habit_no_reward(True, "Награда", None) # ValidationError
        >>> validate_pleasant_habit_no_reward(False, "Награда", None) # OK
    """
    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            'Приятная привычка не может иметь вознаграждение '
            'или связанную привычку.'
        )


def validate_periodicity(periodicity: int) -> None:
    """
    Validator 5: Нельзя выполнять привычку реже, чем 1 раз в 7 дней.

    Regula: 1 <= periodicity <= 7

    Args:
        periodicity: Periodicitatea în zile

    Raises:
        ValidationError: Dacă periodicity nu este între 1 și 7

    Examples:
        >>> validate_periodicity(1)  # OK (zilnic)
        >>> validate_periodicity(7)  # OK (săptămânal)
        >>> validate_periodicity(4)  # OK
        >>> validate_periodicity(0)  # ValidationError
        >>> validate_periodicity(8)  # ValidationError
    """
    if not (1 <= periodicity <= 7):
        raise ValidationError(
            f'Периодичность должна быть от 1 до 7 дней включительно. '
            f'Указано: {periodicity} дней.'
        )
