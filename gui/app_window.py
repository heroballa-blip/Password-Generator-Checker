from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
from tabs.password_tab import PasswordGeneratorTab
from tabs.indevelopment_tab import InDevelopment
from PyQt5.QTCore import Qt
from PyQt5.QtGui import QIcon

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.activateWindow()
        self.raise_()
        

        self.setWindowTitle("Secure Tools(v1.0)")
        self.setGeometry(300, 200, 1000, 400)
        self.setMinimumWidth(1000)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
    
        # Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #e0e0e0;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        self.btn_password = QPushButton("Password Generator")
        self.btn_password.setFixedHeight(40)
        self.btn_dev = QPushButton("In Development!")
        self.btn_dev.setFixedHeight(40)

        sidebar_layout.addWidget(self.btn_password)
        sidebar_layout.addWidget(self.btn_dev)
        sidebar_layout.addStretch()

        # Pages
        self.pages = QStackedWidget()
        self.pages.addWidget(PasswordGeneratorTab())  # 0
        self.pages.addWidget(InDevelopment())

        self.btn_password.clicked.connect(lambda: self.switch_page(0))
        self.btn_dev.clicked.connect(lambda: self.switch_page(1))

        sidebar_widget.setFixedWidth(200)
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages, stretch=1)

        self.sidebar_buttons = [self.btn_password, self.btn_dev,]
        self.switch_page(0)
        self.show()
    def switch_page(self, index: int):
        self.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.sidebar_buttons):
            if i == index:
                btn.setStyleSheet("background-color: #c0c0c0; font-weight: bold;")
            else:
                btn.setStyleSheet("")
    