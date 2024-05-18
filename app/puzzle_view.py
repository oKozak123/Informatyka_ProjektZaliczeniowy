import random
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QPointF
from puzzle_piece import PuzzlePiece

class PuzzleView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QGraphicsView {
                background-color: #4A4A4A;
                border: 2px solid #777777;
                border-radius: 15px;
            }
        """)
        self.current_image_path = None
        self.zoom_factor = 1.0
        self.last_scroll_up = False

    def wheelEvent(self, event):
        max_zoom = 4.0
        min_zoom = 0.25

        zoom_in_factor = 1.1
        zoom_out_factor = 0.9

        if event.angleDelta().y() > 0:
            # Zoom in
            if not self.last_scroll_up:
                self.zoom_factor = 1.0
            self.zoom_factor *= zoom_in_factor
            if self.zoom_factor > max_zoom:
                self.zoom_factor = max_zoom
            self.last_scroll_up = True
        else:
            # Zoom out
            if self.last_scroll_up:
                self.zoom_factor = 1.0
            self.zoom_factor *= zoom_out_factor
            if self.zoom_factor < min_zoom:
                self.zoom_factor = min_zoom
            self.last_scroll_up = False

        self.scale(self.zoom_factor, self.zoom_factor)

    def createPuzzle(self, image_path, num_pieces):
        self.current_image_path = image_path
        image = QPixmap(image_path)
        if image.isNull():
            QMessageBox.critical(self, "Error", "Nie udało się załadować obrazka")
            return

        num_rows = num_cols = int(num_pieces ** 0.5)

        piece_width = image.width() // num_cols
        piece_height = image.height() // num_rows

        pieces = []
        positions = [(col * piece_width, row * piece_height) for row in range(num_rows) for col in range(num_cols)]
        random.shuffle(positions)

        for row in range(num_rows):
            for col in range(num_cols):
                piece = image.copy(col * piece_width, row * piece_height, piece_width, piece_height)
                piece_item = PuzzlePiece(piece, row * num_cols + col)
                piece_item.setPos(*positions.pop())
                self.scene.addItem(piece_item)
                pieces.append(piece_item)

        self.pieces = pieces
        self.scene.setSceneRect(0, 0, num_cols * piece_width, num_rows * piece_height)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def puzzleSolved(self):
        for piece in self.pieces:
            correct_pos = QPointF((piece.index % len(self.pieces)) * piece.pixmap().width(),
                                 (piece.index // len(self.pieces)) * piece.pixmap().height())
            if (piece.pos() - correct_pos).manhattanLength() > 10:
                return False
        return True

    def savePuzzleImage(self):
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()

        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz Zapuzzlowane", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_name:
            image.save(file_name)

    def refreshPuzzle(self, num_pieces):
        if self.current_image_path:
            self.scene.clear()
            self.createPuzzle(self.current_image_path, num_pieces)
