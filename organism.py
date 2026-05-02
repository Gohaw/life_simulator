
"""
Модуль organism.py
Содержит базовый класс Organism и его подклассы:
Plant, Herbivore, Carnivore.
"""

from abc import ABC, abstractmethod
import random


class Organism(ABC):
    """
    Базовый класс для всех организмов в симуляции.
    Атрибуты:
        name (str): название организма.
        energy (int): текущий уровень энергии.
        age (int): возраст организма в днях.
        alive (bool): жив ли организм.
    """

    def __init__(self, name: str, energy: int, age: int = 0):
        self.name = name
        self.energy = energy
        self.age = age
        self.alive = True

    def is_alive(self) -> bool:
        """Возвращает True, если организм жив."""
        return self.alive

    def update_state(self):
        """
        Ежедневное обновление состояния.
        Увеличивает возраст и уменьшает энергию на 1.
        Если энергия <= 0, организм умирает.
        """
        self.age += 1
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False

    @abstractmethod
    def eat(self, food: 'Organism') -> int:
        """
        Абстрактный метод питания.
        Принимает другой организм в качестве пищи.
        Возвращает количество полученной энергии.
        """
        pass

    def __str__(self) -> str:
        status = "жив" if self.alive else "мёртв"
        return f"{self.name} (энергия: {self.energy}, возраст: {self.age}, статус: {status})"


class Plant(Organism):
    """
    Растение. Не ест другие организмы, а получает энергию от солнца.
    Может размножаться, если достаточно энергии.
    """

    def __init__(self, name: str, energy: int = 10, age: int = 0):
        super().__init__(name, energy, age)
        self.sun_energy = 3  # энергия от солнца за день

    def eat(self, food: Organism = None) -> int:
        """
        Растение не ест других. Получает энергию от солнца.
        Возвращает количество полученной энергии.
        """
        self.energy += self.sun_energy
        return self.sun_energy

    def can_reproduce(self) -> bool:
        """Проверяет, может ли растение размножиться (энергия >= 15)."""
        return self.energy >= 15 and self.alive

    def reproduce(self) -> 'Plant':
        """
        Создаёт новое растение, тратя энергию родителя.
        Возвращает новый экземпляр Plant.
        """
        self.energy -= 5
        return Plant(f"Трава_{random.randint(1, 1000)}", energy=8)


class Herbivore(Organism):
    """
    Травоядное животное. Ест только растения.
    Может размножаться при достаточной энергии.
    """

    def __init__(self, name: str, energy: int, age: int = 0):
        super().__init__(name, energy, age)
        self.food_bonus = 5

    def eat(self, food: Organism) -> int:
        """
        Пытается съесть растение.
        Если food — растение и жив, получает энергию.
        Возвращает количество полученной энергии.
        """
        if isinstance(food, Plant) and food.alive:
            gained = self.food_bonus
            self.energy += gained
            food.alive = False  # растение съедено
            return gained
        return 0

    def can_reproduce(self) -> bool:
        """Проверяет, может ли травоядное размножиться (энергия >= 25)."""
        return self.energy >= 25 and self.alive

    def reproduce(self) -> 'Herbivore':
        """Создаёт новое травоядное, тратя энергию родителя."""
        self.energy -= 10
        return Herbivore(f"Кролик_{random.randint(1, 1000)}", energy=15)


class Carnivore(Organism):
    """
    Хищник. Ест травоядных.
    Может размножаться при достаточной энергии.
    """

    def __init__(self, name: str, energy: int, age: int = 0):
        super().__init__(name, energy, age)
        self.food_bonus = 8
        self.hunt_chance = 0.7  # 70% шанс успешной охоты

    def eat(self, food: Organism) -> int:
        """
        Пытается съесть травоядное.
        Шанс успеха зависит от hunt_chance.
        Если охота успешна — получает энергию.
        Возвращает количество полученной энергии.
        """
        if isinstance(food, Herbivore) and food.alive:
            if random.random() < self.hunt_chance:
                gained = self.food_bonus
                self.energy += gained
                food.alive = False
                return gained
        return 0

    def can_reproduce(self) -> bool:
        """Проверяет, может ли хищник размножиться (энергия >= 35)."""
        return self.energy >= 35 and self.alive

    def reproduce(self) -> 'Carnivore':
        """Создаёт нового хищника, тратя энергию родителя."""
        self.energy -= 15
        return Carnivore(f"Лиса_{random.randint(1, 1000)}", energy=20)