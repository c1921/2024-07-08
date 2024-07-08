from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

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
