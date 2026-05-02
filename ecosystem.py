
"""
Модуль ecosystem.py
Содержит класс Ecosystem, управляющий популяциями организмов
и симулирующий ежедневные взаимодействия.
"""

import random
from organism import Organism, Plant, Herbivore, Carnivore


class Ecosystem:
    """
    Класс, моделирующий замкнутую экосистему.
    Хранит список всех организмов и управляет их
    ежедневным циклом жизни.
    """

    def __init__(self):
        """Инициализирует пустую экосистему."""
        self.organisms: list[Organism] = []

    def add_organism(self, organism: Organism) -> None:
        """
        Добавляет организм в экосистему.
        Args:
            organism: экземпляр Organism или его подкласса.
        """
        self.organisms.append(organism)

    def remove_dead(self) -> int:
        """
        Удаляет всех мёртвых организмов из списка.
        Returns:
            Количество удалённых организмов.
        """
        initial_count = len(self.organisms)
        self.organisms = [org for org in self.organisms if org.is_alive()]
        removed = initial_count - len(self.organisms)
        if removed > 0:
            print(f"  [Удалено мёртвых: {removed}]")
        return removed

    def _get_live_plants(self) -> list[Plant]:
        """Возвращает список живых растений."""
        return [org for org in self.organisms if isinstance(org, Plant) and org.is_alive()]

    def _get_live_herbivores(self) -> list[Herbivore]:
        """Возвращает список живых травоядных."""
        return [org for org in self.organisms if isinstance(org, Herbivore) and org.is_alive()]

    def _get_live_carnivores(self) -> list[Carnivore]:
        """Возвращает список живых хищников."""
        return [org for org in self.organisms if isinstance(org, Carnivore) and org.is_alive()]

    def _handle_feeding(self):
        """
        Логика питания для одного дня:
        1. Растения получают энергию от солнца.
        2. Травоядные пытаются съесть растения.
        3. Хищники пытаются съесть травоядных.
        """
        plants = self._get_live_plants()
        herbivores = self._get_live_herbivores()
        carnivores = self._get_live_carnivores()

        # Растения питаются солнцем
        for plant in plants:
            gained = plant.eat()
            print(f"  {plant.name} получает {gained} энергии от солнца.")

        # Травоядные едят растения
        for herb in herbivores:
            if plants:
                target = random.choice(plants)
                gained = herb.eat(target)
                if gained > 0:
                    print(f"  {herb.name} съедает {target.name} и получает {gained} энергии.")
                else:
                    print(f"  {herb.name} не смог поесть.")
            else:
                print(f"  {herb.name} не нашёл растений.")

        # Хищники охотятся на травоядных
        for carn in carnivores:
            if herbivores:
                target = random.choice(herbivores)
                gained = carn.eat(target)
                if gained > 0:
                    print(f"  {carn.name} охотится на {target.name} и получает {gained} энергии.")
                else:
                    print(f"  {carn.name} не смог поймать {target.name}.")
            else:
                print(f"  {carn.name} не нашёл добычи.")

    def _handle_reproduction(self):
        """
        Логика размножения для одного дня.
        Организмы с достаточной энергией создают потомство.
        """
        new_organisms = []

        for org in self.organisms:
            if not org.is_alive():
                continue

            if isinstance(org, Plant) and org.can_reproduce():
                child = org.reproduce()
                new_organisms.append(child)
                print(f"  {org.name} размножается! Появилось новое растение: {child.name}")

            elif isinstance(org, Herbivore) and org.can_reproduce():
                child = org.reproduce()
                new_organisms.append(child)
                print(f"  {org.name} размножается! Появился новый: {child.name}")

            elif isinstance(org, Carnivore) and org.can_reproduce():
                child = org.reproduce()
                new_organisms.append(child)
                print(f"  {org.name} размножается! Появился новый: {child.name}")

        self.organisms.extend(new_organisms)

    def simulate_day(self) -> None:
        """
        Симулирует один день в экосистеме:
        1. Питание
        2. Обновление состояния (старение, расход энергии)
        3. Размножение
        Порядок важен: сначала еда, потом старение,
        чтобы новорождённые не умирали в тот же день.
        """
        self._handle_feeding()
        for org in self.organisms:
            org.update_state()
        self._handle_reproduction()

    def get_stats(self) -> dict:
        """
        Возвращает статистику по текущему состоянию экосистемы.
        Returns:
            Словарь с количеством растений, травоядных, хищников и общим числом.
        """
        plants = len(self._get_live_plants())
        herbivores = len(self._get_live_herbivores())
        carnivores = len(self._get_live_carnivores())
        total = plants + herbivores + carnivores

        return {
            "plants": plants,
            "herbivores": herbivores,
            "carnivores": carnivores,
            "total": total
        }

    def __str__(self) -> str:
        stats = self.get_stats()
        return (
            f"Экосистема: {stats['total']} организмов "
            f"(🌱 {stats['plants']}, 🐇 {stats['herbivores']}, 🦊 {stats['carnivores']})"
        )