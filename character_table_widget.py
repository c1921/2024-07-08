from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from character import Character

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
