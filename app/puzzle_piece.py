from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import Qt

class PuzzlePiece(QGraphicsPixmapItem):
    def __init__(self, pixmap, index, parent=None):
        super().__init__(pixmap, parent)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
        self.index = index
        self.initial_pos = None

    def hoverEnterEvent(self, event):
        self.setOpacity(0.7)

    def hoverLeaveEvent(self, event):
        self.setOpacity(1.0)

    def mousePressEvent(self, event):
        self.initial_pos = self.pos()
        self.bringToFront()
        super().mousePressEvent(event)

    def bringToFront(self):
        top_z = max([item.zValue() for item in self.scene().items()]) + 1
        self.setZValue(top_z)

    def mouseReleaseEvent(self, event):
        colliding_items = self.collidingItems(Qt.IntersectsItemBoundingRect)
        if colliding_items:
            closest_piece = min(colliding_items, key=lambda item: (item.pos() - self.pos()).manhattanLength())
            closest_piece_pos = closest_piece.pos()
            closest_piece.setPos(self.initial_pos)
            self.setPos(closest_piece_pos)
        else:
            self.setPos(self.initial_pos)
        super().mouseReleaseEvent(event)
