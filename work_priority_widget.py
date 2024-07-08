from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt

class WorkPriorityWidget(QWidget):
    def __init__(self, characters):
        super().__init__()
        self.characters = characters
        self.work_types = ["Farming", "Crafting"]
        
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        # 设置表头
        grid_layout.addWidget(QLabel("Work"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        for i, work_type in enumerate(self.work_types, start=1):
            grid_layout.addWidget(QLabel(work_type), 0, i + 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 填充角色名字和优先级选择
        for i, character in enumerate(characters, start=1):
            grid_layout.addWidget(QLabel(character.name), i, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            for j, work_type in enumerate(self.work_types, start=1):
                combo_box = QComboBox()
                combo_box.addItems(["1", "2", "3", "4", "Prohibited"])
                combo_box.setCurrentIndex(character.priority[work_type] - 1)
                combo_box.currentIndexChanged.connect(self.update_priority(character, work_type))
                grid_layout.addWidget(combo_box, i, j + 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(20)
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)
    
    def update_priority(self, character, work_type):
        def handler(index):
            if index == 4:
                character.priority[work_type] = 5  # Prohibited
            else:
                character.priority[work_type] = index + 1
        return handler
