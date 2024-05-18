from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal

class puzzle_quantity_events(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_value = 1
        self.layout = QHBoxLayout()
        self.label = QLabel("Puzzle: ")
        self.layout.addWidget(self.label)
        self.counter_label = QLabel(str(self.current_value))
        self.layout.addWidget(self.counter_label)
        self.increase_button = QPushButton("+")
        self.increase_button.clicked.connect(self.increase_value)
        self.layout.addWidget(self.increase_button)
        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_value)
        self.layout.addWidget(self.decrease_button)

        self.setLayout(self.layout)

    def set_value(self, value):
        self.current_value = value
        self.counter_label.setText(str(self.current_value))
        self.value_changed.emit(self.current_value)

    def increase_value(self):
        self.current_value += 1
        while not self.is_pierwiastek(self.current_value):
            self.current_value += 1
        self.counter_label.setText(str(self.current_value))
        self.value_changed.emit(self.current_value)

    def decrease_value(self):
        if self.current_value > 1:
            self.current_value -= 1
            while not self.is_pierwiastek(self.current_value):
                self.current_value -= 1
            self.counter_label.setText(str(self.current_value))
            self.value_changed.emit(self.current_value)

    def value(self):
        return self.current_value

    def is_pierwiastek(self, n):
        return int(n ** 0.5) ** 2 == n
