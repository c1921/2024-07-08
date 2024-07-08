import random
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QHBoxLayout, QProgressBar, QGridLayout, QTabWidget,
    QComboBox, QPushButton
)
from PyQt6.QtCore import QTimer

# 角色类
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

# 角色表格窗口
class CharacterTableWidget(QWidget):
    def __init__(self, characters):
        super().__init__()
        layout = QVBoxLayout()
        
        # 创建表格
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(characters))
        self.table_widget.setColumnCount(11)  # Name, Age, and 9 skills
        
        # 设置表头
        self.table_widget.setHorizontalHeaderLabels([
            "Name", "Age", "Construction", "Farming", "Blacksmithing", "Tailoring",
            "Cooking", "Crafting", "Art", "Medicine", "Combat"
        ])
        
        # 填充表格数据
        for row, character in enumerate(characters):
            self.table_widget.setItem(row, 0, QTableWidgetItem(character.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(character.age)))
            for col, (skill, level) in enumerate(character.skills.items(), start=2):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(level)))
        
        # 禁用用户编辑表格
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

# 土地界面窗口
class LandWidget(QWidget):
    def __init__(self, characters):
        super().__init__()
        self.characters = characters
        self.total_land = 0
        self.current_land = 0
        
        layout = QVBoxLayout()
        
        # 输入预期耕地的布局
        input_layout = QHBoxLayout()
        self.land_input = QLineEdit()
        self.land_input.setPlaceholderText("Enter expected farmland value")
        self.land_input.returnPressed.connect(self.assign_work)
        input_layout.addWidget(self.land_input)
        
        # 进度条布局
        self.progress_layout = QGridLayout()
        
        layout.addLayout(input_layout)
        layout.addLayout(self.progress_layout)
        self.setLayout(layout)
        
        # 设置计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        
    def assign_work(self):
        try:
            self.total_land = int(self.land_input.text())
            self.current_land = 0
            self.progress_layout.setRowStretch(len(self.characters), 1)
            
            for i, character in enumerate(self.characters):
                character.progress_bar.setMaximum(100)
                character.progress_bar.setValue(0)
                self.progress_layout.addWidget(QLabel(character.name), i, 0)
                self.progress_layout.addWidget(character.progress_bar, i, 1)
                self.progress_layout.addWidget(character.status_label, i, 2)
                character.progress = 0
                character.time_per_unit = 10 / max(1, character.skills["Farming"])
            
            self.timer.start(100)  # 每100毫秒更新一次
        except ValueError:
            self.progress_layout.addWidget(QLabel("Please enter a valid number"), 0, 0)
    
    def update_progress(self):
        all_done = True
        for character in self.characters:
            if self.current_land < self.total_land:
                all_done = False
                character.progress += 100 / (character.time_per_unit * 10)
                if character.progress >= 100:
                    character.progress = 0
                    self.current_land += 1
                    if self.current_land >= self.total_land:
                        character.status_label.setText("Idle")
                    else:
                        character.status_label.setText("Working")
                character.progress_bar.setValue(int(character.progress))
            else:
                character.status_label.setText("Idle")
        
        if all_done:
            self.timer.stop()

# 手工制作界面
class CraftingWidget(QWidget):
    def __init__(self, characters, storage_widget):
        super().__init__()
        self.characters = characters
        self.storage_widget = storage_widget
        self.storage = storage_widget.storage
        
        layout = QVBoxLayout()
        
        # 创建手工品选择和数量输入
        input_layout = QHBoxLayout()
        self.craft_item_select = QComboBox()
        self.craft_item_select.addItems(["Toy", "Basket", "Chair", "Table"])
        self.craft_quantity_input = QLineEdit()
        self.craft_quantity_input.setPlaceholderText("Enter quantity to craft")
        self.craft_button = QPushButton("Craft")
        self.craft_button.clicked.connect(self.assign_craft_work)
        input_layout.addWidget(self.craft_item_select)
        input_layout.addWidget(self.craft_quantity_input)
        input_layout.addWidget(self.craft_button)
        
        # 进度条布局
        self.progress_layout = QGridLayout()
        
        layout.addLayout(input_layout)
        layout.addLayout(self.progress_layout)
        self.setLayout(layout)
        
        # 设置计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
    
    def assign_craft_work(self):
        try:
            self.total_crafts = int(self.craft_quantity_input.text())
            self.current_crafts = 0
            self.progress_layout.setRowStretch(len(self.characters), 1)
            self.craft_item = self.craft_item_select.currentText()
            
            for i, character in enumerate(self.characters):
                character.progress_bar.setMaximum(100)
                character.progress_bar.setValue(0)
                self.progress_layout.addWidget(QLabel(character.name), i, 0)
                self.progress_layout.addWidget(character.progress_bar, i, 1)
                self.progress_layout.addWidget(character.status_label, i, 2)
                character.progress = 0
                character.time_per_unit = 10 / max(1, character.skills["Crafting"])
            
            self.timer.start(100)  # 每100毫秒更新一次
        except ValueError:
            self.progress_layout.addWidget(QLabel("Please enter a valid number"), 0, 0)
    
    def update_progress(self):
        all_done = True
        for character in self.characters:
            if self.current_crafts < self.total_crafts:
                all_done = False
                character.progress += 100 / (character.time_per_unit * 10)
                if character.progress >= 100:
                    character.progress = 0
                    self.current_crafts += 1
                    self.storage[self.craft_item] = self.storage.get(self.craft_item, 0) + 1
                    self.storage_widget.update_storage()
                    if self.current_crafts >= self.total_crafts:
                        character.status_label.setText("Idle")
                    else:
                        character.status_label.setText("Working")
                character.progress_bar.setValue(int(character.progress))
            else:
                character.status_label.setText("Idle")
        
        if all_done:
            self.timer.stop()

# 仓储界面
class StorageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.storage = {}
        layout = QVBoxLayout()
        self.storage_table = QTableWidget()
        self.storage_table.setColumnCount(2)
        self.storage_table.setHorizontalHeaderLabels(["Item", "Quantity"])
        layout.addWidget(self.storage_table)
        self.setLayout(layout)
    
    def update_storage(self):
        self.storage_table.setRowCount(len(self.storage))
        for row, (item, quantity) in enumerate(self.storage.items()):
            self.storage_table.setItem(row, 0, QTableWidgetItem(item))
            self.storage_table.setItem(row, 1, QTableWidgetItem(str(quantity)))

# 主窗口
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

# 主函数
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
