# src/ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItemGroup, QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from src.config import GridConfig
from src.core.map_generator import MapGenerator
from src.ui.widgets.toolbar import TopToolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HexaMapForge")
        self.resize(1000, 800)
        self.init_ui()

    def init_ui(self):
        # --- Crear barra superior ---
        self.toolbar = TopToolbar(on_action=self.handle_toolbar_action)

        # --- Crear vista de escena ---
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints() | self.view.renderHints().Antialiasing)
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Estilo de fondo
        palette = self.view.palette()
        palette.setColor(QPalette.Base, QColor("#f0f0f0"))
        self.view.setPalette(palette)

        # --- Generar mapa de hexágonos ---
        map_gen = MapGenerator(rows=3, cols=4, tile_size=30)
        tiles = map_gen.generate()

        # Agrupar todos los hexágonos
        group = QGraphicsItemGroup()
        for tile in tiles:
            group.addToGroup(tile)
        self.scene.addItem(group)

        # Centrar grupo
        self.center_group(group)

        # --- Layout principal con toolbar y vista ---
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)
        self.setCentralWidget(central_widget)

    def center_group(self, group):
        """Centrar el grupo de hexágonos dentro de la vista."""
        view_size = self.view.viewport().size()
        group_rect = group.boundingRect()

        dx = (view_size.width() - group_rect.width()) / 2 - group_rect.x()
        dy = (view_size.height() - group_rect.height()) / 2 - group_rect.y()

        group.setPos(dx, dy)

    def handle_toolbar_action(self, action_name):
        print(f"Acción del toolbar: {action_name}")
        # Aquí puedes manejar herramientas seleccionadas, color, etc.
