"""
Модуль тестирования базовой логики симуляции.
Тесты для классов Organism, Plant, Herbivore, Carnivore и Ecosystem.
"""

import unittest
import sys
import os

# Добавляем корневую папку в путь для импорта модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from organism import Organism, Plant, Herbivore, Carnivore
from ecosystem import Ecosystem


class TestOrganism(unittest.TestCase):
    """Тесты базового класса Organism и его наследников."""

    def test_plant_creation(self):
        """Проверка создания растения."""
        plant = Plant("ТестТрава", energy=10)
        self.assertEqual(plant.name, "ТестТрава")
        self.assertEqual(plant.energy, 10)
        self.assertTrue(plant.is_alive())

    def test_herbivore_creation(self):
        """Проверка создания травоядного."""
        rabbit = Herbivore("ТестКролик", energy=20)
        self.assertEqual(rabbit.name, "ТестКролик")
        self.assertEqual(rabbit.energy, 20)
        self.assertTrue(rabbit.is_alive())

    def test_carnivore_creation(self):
        """Проверка создания хищника."""
        fox = Carnivore("ТестЛиса", energy=30)
        self.assertEqual(fox.name, "ТестЛиса")
        self.assertEqual(fox.energy, 30)
        self.assertTrue(fox.is_alive())

    def test_plant_eat_sun(self):
        """Растение получает энергию от солнца."""
        plant = Plant("Трава", energy=5)
        gained = plant.eat()
        self.assertEqual(gained, 3)
        self.assertEqual(plant.energy, 8)

    def test_herbivore_eat_plant(self):
        """Травоядное съедает растение."""
        plant = Plant("Трава", energy=10)
        rabbit = Herbivore("Кролик", energy=20)
        gained = rabbit.eat(plant)
        self.assertEqual(gained, 5)
        self.assertEqual(rabbit.energy, 25)
        self.assertFalse(plant.is_alive())

    def test_carnivore_hunt_success(self):
        """Хищник успешно охотится (с вероятностью 100% для теста)."""
        rabbit = Herbivore("Кролик", energy=20)
        fox = Carnivore("Лиса", energy=30)
        fox.hunt_chance = 1.0  # гарантируем успех
        gained = fox.eat(rabbit)
        self.assertEqual(gained, 8)
        self.assertEqual(fox.energy, 38)
        self.assertFalse(rabbit.is_alive())

    def test_carnivore_hunt_fail(self):
        """Хищник промахивается (шанс 0%)."""
        rabbit = Herbivore("Кролик", energy=20)
        fox = Carnivore("Лиса", energy=30)
        fox.hunt_chance = 0.0  # гарантируем провал
        gained = fox.eat(rabbit)
        self.assertEqual(gained, 0)
        self.assertEqual(fox.energy, 30)
        self.assertTrue(rabbit.is_alive())

    def test_organism_death(self):
        """Организм умирает при энергии <= 0."""
        plant = Plant("Трава", energy=1)
        plant.update_state()  # энергия становится 0
        self.assertFalse(plant.is_alive())

    def test_plant_reproduction(self):
        """Растение размножается при энергии >= 15."""
        plant = Plant("Трава", energy=20)
        self.assertTrue(plant.can_reproduce())
        child = plant.reproduce()
        self.assertEqual(plant.energy, 15)  # потрачено 5
        self.assertIsInstance(child, Plant)
        self.assertTrue(child.is_alive())

    def test_herbivore_reproduction(self):
        """Травоядное размножается при энергии >= 25."""
        rabbit = Herbivore("Кролик", energy=30)
        self.assertTrue(rabbit.can_reproduce())
        child = rabbit.reproduce()
        self.assertEqual(rabbit.energy, 20)  # потрачено 10
        self.assertIsInstance(child, Herbivore)

    def test_carnivore_reproduction(self):
        """Хищник размножается при энергии >= 35."""
        fox = Carnivore("Лиса", energy=40)
        self.assertTrue(fox.can_reproduce())
        child = fox.reproduce()
        self.assertEqual(fox.energy, 25)  # потрачено 15
        self.assertIsInstance(child, Carnivore)


class TestEcosystem(unittest.TestCase):
    """Тесты класса Ecosystem."""

    def setUp(self):
        """Создаёт чистую экосистему перед каждым тестом."""
        self.eco = Ecosystem()

    def test_add_organism(self):
        """Добавление организма в экосистему."""
        plant = Plant("Трава", energy=10)
        self.eco.add_organism(plant)
        self.assertEqual(len(self.eco.organisms), 1)

    def test_remove_dead(self):
        """Удаление мёртвых организмов."""
        plant = Plant("Трава", energy=1)
        self.eco.add_organism(plant)
        plant.update_state()  # умерла
        removed = self.eco.remove_dead()
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.eco.organisms), 0)

    def test_get_stats(self):
        """Проверка статистики экосистемы."""
        self.eco.add_organism(Plant("Трава", energy=10))
        self.eco.add_organism(Herbivore("Кролик", energy=20))
        self.eco.add_organism(Carnivore("Лиса", energy=30))
        stats = self.eco.get_stats()
        self.assertEqual(stats["plants"], 1)
        self.assertEqual(stats["herbivores"], 1)
        self.assertEqual(stats["carnivores"], 1)
        self.assertEqual(stats["total"], 3)

    def test_simulate_day_runs(self):
        """Проверка, что симуляция дня не вызывает ошибок."""
        self.eco.add_organism(Plant("Трава", energy=10))
        self.eco.add_organism(Herbivore("Кролик", energy=20))
        # Не должно быть исключений
        try:
            self.eco.simulate_day()
            self.eco.remove_dead()
        except Exception as e:
            self.fail(f"simulate_day вызвал ошибку: {e}")


if __name__ == "__main__":
    unittest.main()
