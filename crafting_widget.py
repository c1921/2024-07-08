from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QGridLayout, QComboBox, QPushButton
from PyQt6.QtCore import QTimer

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
