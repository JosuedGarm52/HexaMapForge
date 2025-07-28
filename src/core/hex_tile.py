import math
from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsItem
from PySide6.QtGui import QPolygonF, QBrush, QColor
from PySide6.QtCore import QPointF


class HexTile(QGraphicsPolygonItem):
    def __init__(self, q, r, size=30, color="#cccccc"):
        super().__init__()

        self.q = q
        self.r = r
        self.s = -q - r  # Coordenada cúbica derivada
        self.size = size
        self.color = QColor(color)

        self.setPolygon(self.create_hexagon())
        self.setBrush(QBrush(self.color))
        self.setPen(QColor("black"))
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # Posicionar visualmente según la grilla cúbica
        pos = self.hex_to_pixel()
        self.setPos(pos.x(), pos.y())

    def hex_to_pixel(self):
        """Posición en píxeles para hexágono puntiagudo arriba (vertical)"""
        width = math.sqrt(3) * self.size
        height = self.size * 2
        x = width * (self.q + self.r/2)
        y = height * 3/4 * self.r
        return QPointF(x, y)

    def create_hexagon(self):
        """Crea un polígono con forma de hexágono regular."""
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30  # Orientación plana arriba
            angle_rad = math.radians(angle_deg)
            x = self.size * math.cos(angle_rad)
            y = self.size * math.sin(angle_rad)
            points.append(QPointF(x, y))

        return QPolygonF(points)

    def set_color(self, color_hex):
        """Cambia el color de relleno del hexágono."""
        self.color = QColor(color_hex)
        self.setBrush(QBrush(self.color))
