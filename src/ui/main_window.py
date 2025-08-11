# src/ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItemGroup, QWidget, QVBoxLayout,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
import traceback

from src.config import GridConfig
from src.core.map_generator import MapGenerator

from src.ui.widgets.Toolbar.Toolbar import Toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HexaMapForge")
        self.resize(1000, 800)
        try:
            self.setup_ui()
        except Exception as e:
            print("Error durante la inicialización de la UI:", e)
            traceback.print_exc()
            self.show_error_dialog(str(e))

    def setup_ui(self):
        # --- Crear barra superior ---
        self.toolbar = Toolbar(
            config_path="src/config/toolbar_config.json",
            on_action_callback=self.handle_toolbar_action,
            background_color="#f0f0f0",
            header_bg="#bbbbbb",
            child_bg="#e6e6e6",
            max_visible=3,
            orientation="horizontal"
        )

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

    def show_error_dialog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error al iniciar la aplicación")
        dlg.setIcon(QMessageBox.Critical)
        dlg.setText("Ocurrió un error al inicializar la aplicación:")
        dlg.setInformativeText(message)
        dlg.exec()
