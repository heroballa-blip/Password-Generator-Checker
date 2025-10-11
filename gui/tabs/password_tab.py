from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSpinBox, QCheckBox, QTextEdit, QMessageBox, QLineEdit, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from utils.dictionary_utils import load_dictionary
from utils.entropy_utils import adjusted_strength
from utils.generation_utils import generate_password


class PasswordGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        try:
            self.dictionary = load_dictionary()
        except Exception as e:
            self.dictionary: set[str] = set()
            QMessageBox.warning(self, "Warning", f"Could not load dictionary: {e}")

        # Controls Row
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Set Password Length (Min 16):"))

        self.length_spin = QSpinBox()
        self.length_spin.setMinimum(16)
        self.length_spin.setMaximum(128)
        self.length_spin.setValue(16)
        self.length_spin.setFixedWidth(60)
        top_row.addWidget(self.length_spin)

        self.exclude_special_checkbox = QCheckBox("Exclude Special")
        self.exclude_numbers_checkbox = QCheckBox("Exclude Numbers")
        self.exclude_letters_checkbox = QCheckBox("Exclude Letters")

        top_row.addWidget(self.exclude_special_checkbox)
        top_row.addWidget(self.exclude_numbers_checkbox)
        top_row.addWidget(self.exclude_letters_checkbox)
        layout.addLayout(top_row)

        # Generate Button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.setFixedHeight(35)
        self.generate_button.clicked.connect(self.on_generate)
        layout.addWidget(self.generate_button)

        # Password Output
        self.result_box = QTextEdit()
        self.result_box.setFont(QFont("Menlo", 12))
        self.result_box.setFixedHeight(60)
        self.result_box.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                padding: 6px;
                font-weight: bold;
            }
        """)
        self.result_box.textChanged.connect(self.on_password_edit)
        layout.addWidget(self.result_box)

        # Strength Meter
        self.strength_boxes: list[QLabel] = []
        strength_row = QHBoxLayout()
        self.strength_boxes = []
        for _ in range(5):
            box = QLabel()
            box.setFixedSize(30, 20)
            box.setStyleSheet("background-color: #ddd; border: 1px solid #aaa;")
            strength_row.addWidget(box)
            self.strength_boxes.append(box)
        strength_row.addStretch()
        layout.addLayout(strength_row)

        self.strength_label = QLabel("Strength: -")
        layout.addWidget(self.strength_label)

        # Entropy Row
        entropy_row = QHBoxLayout()
        entropy_row.addWidget(QLabel("Entropy:"))
        self.entropy_box = QLineEdit()
        self.entropy_box.setReadOnly(True)
        self.entropy_box.setFixedWidth(150)
        self.entropy_box.setFixedHeight(28)
        self.entropy_box.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                padding: 4px;
                font-weight: bold;
            }
        """)
        entropy_row.addWidget(self.entropy_box)
        entropy_row.addStretch()
        layout.addLayout(entropy_row)

        # Copy Button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setFixedHeight(30)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setEnabled(False)
        layout.addWidget(self.copy_button)

        layout.addStretch()
        self.setLayout(layout)

    # Strength Helpers
    def classify_strength(self, entropy: float) -> tuple[int, str, float]:
        if entropy < 72:
            return 1, "Very Weak", 0.0
        elif entropy < 100:
            return 2, "Weak", 0.25
        elif entropy < 128:
            return 3, "Medium", 0.5
        elif entropy < 175:
            return 4, "Strong", 0.75
        else:
            return 5, "Very Strong", 1.0

    def gradient_color(self, t: float) -> str:
        if t <= 0.5:
            r = 255
            g = int(2 * t * 255)
            b = 0
        else:
            r = int((1 - 2 * (t - 0.5)) * 255)
            g = 255
            b = 0
        return f'rgb({r},{g},{b})'

    def update_strength_meter(self, entropy: float) -> None:        
        level, label, t = self.classify_strength(entropy)
        for box in self.strength_boxes:
            box.setStyleSheet("background-color: #ddd; border: 1px solid #aaa;")
        color = self.gradient_color(t)
        for i in range(min(level, len(self.strength_boxes))):
            self.strength_boxes[i].setStyleSheet(f"background-color: {color}; border: 1px solid #555;")

        self.strength_label.setText(f"Strength: {label}")

    # Event Handlers
    def on_password_edit(self):
        text = self.result_box.toPlainText().strip()
        if not text:
            self.entropy_box.setText("")
            self.update_strength_meter(0)
            self.strength_label.setText("Strength: -")
            return
        strength, entropy = adjusted_strength(text, self.dictionary)
        self.entropy_box.setText(f"{entropy:.2f} bits")
        self.update_strength_meter(entropy)
        self.strength_label.setText(f"Strength: {strength}")

    def on_generate(self):
        length = self.length_spin.value()
        try:
            password = generate_password(
                length,
                self.exclude_special_checkbox.isChecked(),
                self.exclude_numbers_checkbox.isChecked(),
                self.exclude_letters_checkbox.isChecked()
            )
        except ValueError as e:
            self.result_box.setText(str(e))
            self.entropy_box.setText("")
            self.update_strength_meter(0)
            self.copy_button.setEnabled(False)
            return

        if not password:
            self.result_box.setText("Error: All character types excluded.")
            self.entropy_box.setText("")
            self.update_strength_meter(0)
            self.copy_button.setEnabled(False)
            return

        self.result_box.setText(password)
        self.copy_button.setEnabled(True)
        self.generate_button.setText("Password Generated!")
        QTimer.singleShot(1000, lambda: self.generate_button.setText("Generate Password"))

        strength, entropy = adjusted_strength(password, self.dictionary)
        self.entropy_box.setText(f"{entropy:.2f} bits")
        self.update_strength_meter(entropy)
        self.strength_label.setText(f"Strength: {strength}")

    def copy_to_clipboard(self):
        text = self.result_box.toPlainText().strip()
        if text:
            cb = QApplication.clipboard()
            if cb is not None:
                cb.setText(text)
            QMessageBox.information(self, "Copied", "Password copied to clipboard!")
