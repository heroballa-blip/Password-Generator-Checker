from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint

class InDevelopment(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This feature is still in development.")
        label.setAlignment(Qt.Alignment.AlignCenter)
        layout.addWidget(label)
