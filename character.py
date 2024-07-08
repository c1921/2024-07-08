import random
from PyQt6.QtWidgets import QLabel, QProgressBar

class Character:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.skills = {
            "Construction": random.randint(0, 20),
            "Farming": random.randint(0, 20),
            "Blacksmithing": random.randint(0, 20),
            "Tailoring": random.randint(0, 20),
            "Cooking": random.randint(0, 20),
            "Crafting": random.randint(0, 20),
            "Art": random.randint(0, 20),
            "Medicine": random.randint(0, 20),
            "Combat": random.randint(0, 20)
        }
        self.status_label = QLabel("Idle")
        self.progress_bar = QProgressBar()

    def __str__(self):
        skills = ', '.join([f"{k}: {v}" for k, v in self.skills.items()])
        return f"Name: {self.name}, Age: {self.age}, Skills: {skills}"
