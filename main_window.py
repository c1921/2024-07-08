from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from character import Character
from character_table_widget import CharacterTableWidget
from land_widget import LandWidget
from crafting_widget import CraftingWidget
from storage_widget import StorageWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Survival Game")
        self.setGeometry(50, 50, 1000, 700)
        
        self.characters = [
            Character("John", 25),
            Character("Alice", 30),
            Character("Bob", 22),
            Character("Eve", 28)
        ]
        
        self.storage_widget = StorageWidget()
        
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 角色表格标签
        self.character_table = CharacterTableWidget(self.characters)
        self.tabs.addTab(self.character_table, "Character List")
        
        # 土地界面标签
        self.land_widget = LandWidget(self.characters)
        self.tabs.addTab(self.land_widget, "Farming")
        
        # 手工制作界面标签
        self.crafting_widget = CraftingWidget(self.characters, self.storage_widget)
        self.tabs.addTab(self.crafting_widget, "Crafting")
        
        # 仓储界面标签
        self.tabs.addTab(self.storage_widget, "Storage")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
