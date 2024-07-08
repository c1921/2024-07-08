from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QGridLayout
from PyQt6.QtCore import QTimer
from character import Character

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
                if character.priority["Farming"] <= 4:
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
