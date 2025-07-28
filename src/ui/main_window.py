# src/ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItemGroup
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from src.config import GridConfig
from src.core.hex_grid import HexGrid
from src.core.map_generator import MapGenerator

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

        # Crear el mapa de hexágonos
        map_gen = MapGenerator(rows=3, cols=4, tile_size=30)
        tiles = map_gen.generate()

        # Agrupar todos los hexágonos
        group = QGraphicsItemGroup()
        for tile in tiles:
            group.addToGroup(tile)

        self.scene.addItem(group)

        # Centrar el grupo dentro de la escena
        self.center_group(group)

    def center_scene(self):
        """Centra y ajusta la vista para mostrar todo el contenido."""
        bounding_rect = self.scene.itemsBoundingRect()
        self.scene.setSceneRect(bounding_rect)
        self.view.fitInView(bounding_rect, Qt.KeepAspectRatio)

    def center_group(self, group):
        """Centrar el grupo de hexágonos dentro de la ventana."""
        # Tamaño de la escena (igual al tamaño de la ventana)
        scene_width = self.view.viewport().width()
        scene_height = self.view.viewport().height()

        group_rect = group.boundingRect()

        # Calcular el desplazamiento necesario para centrar el grupo
        dx = (scene_width - group_rect.width()) / 2 - group_rect.x()
        dy = (scene_height - group_rect.height()) / 2 - group_rect.y()

        group.setPos(dx, dy)
