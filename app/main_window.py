from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from puzzle_view import PuzzleView
from puzzle_quantity_events import puzzle_quantity_events

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Szyfrowanie Puzzelkowe")
        self.layout = QVBoxLayout()
        self.view = PuzzleView()
        self.layout.addWidget(self.view)

        self.num_pieces_input = puzzle_quantity_events()

        self.num_pieces_input.set_value(1)
        self.num_pieces_input.value_changed.connect(self.updatePuzzle)
        self.layout.addWidget(self.num_pieces_input)

        button_layout = QHBoxLayout()
        import_button = QPushButton("Dodaj Obrazek")
        import_button.clicked.connect(self.importImage)
        button_layout.addWidget(import_button)

        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.saveImage)
        button_layout.addWidget(save_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #3A3A3A;
                color: white;
                font-size: 18px;
            }
            QLabel {
                color: white;
                font-size: 18px;
            }
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #999999;
            }
            QGraphicsView {
                background-color: #4A4A4A;
                border: 2px solid #777777;
                border-radius: 15px;
            }
        """)

    def importImage(self):
        num_pieces = self.num_pieces_input.value()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz Obrazek", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.view.scene.clear()
            self.view.createPuzzle(file_name, num_pieces)

    def saveImage(self):
        self.view.savePuzzleImage()

    def updatePuzzle(self, num_pieces):
        self.view.refreshPuzzle(num_pieces)
