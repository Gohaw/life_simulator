
"""
Модуль utils.py
Вспомогательные функции для симуляции.
"""

import random


def chance(percent: float) -> bool:
    """
    Возвращает True с вероятностью percent (от 0 до 100).
    Используется для случайных событий в симуляции.
    Args:
        percent: вероятность в процентах (0-100).
    Returns:
        True, если событие произошло.
    """
    return random.random() * 100 < percent


def log_event(message: str, level: str = "INFO") -> None:
    """
    Выводит сообщение с префиксом уровня важности.
    Args:
        message: текст сообщения.
        level: уровень (INFO, WARN, EVENT).
    """
    prefix = f"[{level}]"
    print(f"{prefix} {message}")


def print_separator(title: str = "") -> None:
    """
    Выводит разделитель с заголовком для удобства чтения логов.
    Args:
        title: заголовок секции.
    """
    if title:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
    else:
        print("=" * 50)