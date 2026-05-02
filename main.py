"""
Модуль main.py
Точка входа в симулятор жизни.
Запускает симуляцию экосистемы на заданное количество дней.
"""

from ecosystem import Ecosystem
from organism import Plant, Herbivore, Carnivore
from utils import print_separator, log_event


def create_initial_population(eco: Ecosystem) -> None:
    """
    Создаёт начальную популяцию организмов в экосистеме.
    Args:
        eco: экземпляр Ecosystem.
    """
    # Добавляем растения
    for i in range(8):
        eco.add_organism(Plant(f"Трава_{i + 1}", energy=12))

    # Добавляем травоядных
    for i in range(4):
        eco.add_organism(Herbivore(f"Кролик_{i + 1}", energy=25))

    # Добавляем хищников
    for i in range(2):
        eco.add_organism(Carnivore(f"Лиса_{i + 1}", energy=40))

    log_event(f"Создана начальная популяция: {eco}", "INFO")


def run_simulation(days: int = 20) -> None:
    """
    Запускает симуляцию на заданное количество дней.
    Args:
        days: количество дней симуляции.
    """
    eco = Ecosystem()
    create_initial_population(eco)

    for day in range(1, days + 1):
        print_separator(f"День {day}")
        print(f"До симуляции: {eco}")

        eco.simulate_day()
        eco.remove_dead()

        print(f"После симуляции: {eco}")

        # Проверка на вымирание
        stats = eco.get_stats()
        if stats["total"] == 0:
            log_event("Все организмы погибли. Симуляция остановлена.", "EVENT")
            break

        # Предупреждение при низкой популяции
        if stats["total"] < 5:
            log_event("Популяция критически мала!", "WARN")

    print_separator("Итоги симуляции")
    final_stats = eco.get_stats()
    print(f"Растений: {final_stats['plants']}")
    print(f"Травоядных: {final_stats['herbivores']}")
    print(f"Хищников: {final_stats['carnivores']}")
    print(f"Всего выжило: {final_stats['total']}")


def main() -> None:
    """
    Главная функция. Запускает симулятор жизни.
    """
    print_separator("Консольный симулятор жизни")
    print("Модель: хищник-жертва с растениями")
    print("Каждый день организмы питаются, стареют и размножаются.\n")

    run_simulation(days=15)


if __name__ == "__main__":
    main()
