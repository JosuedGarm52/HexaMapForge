# src/ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from src.config import GridConfig
from src.core.hex_grid import HexGrid

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
        self.resize(1000, 800)

        palette = self.view.palette()
        palette.setColor(QPalette.Base, QColor("#f0f0f0"))
        self.view.setPalette(palette)

        # ---- Aquí construimos el mapa rectangular ----
        cfg = GridConfig(cols=12, rows=8, size=30, offset="even-q", orientation="flat")
        self.grid = HexGrid(cfg).build()
        self.grid.add_to_scene(self.scene)
