# src/ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from src.core.hex_tile import HexTile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HexaMapForge")

        self.init_ui()

    def init_ui(self):
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints() | self.view.renderHints().Antialiasing)
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setCentralWidget(self.view)
        self.resize(800, 600)

        palette = self.view.palette()
        palette.setColor(QPalette.Base, QColor("#f0f0f0"))
        self.view.setPalette(palette)

        # Crear un pequeño mapa hexagonal (3 de radio = 37 hexes)
        radius = 3
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q - r
                if abs(s) <= radius:
                    tile = HexTile(q, r, size=30)
                    self.scene.addItem(tile)
