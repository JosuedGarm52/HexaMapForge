# src/ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HexaMapForge")

        self.init_ui()

    def init_ui(self):
        # Crear una escena donde dibujaremos hexágonos
        self.scene = QGraphicsScene(self)

        # Crear una vista para mostrar la escena
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints() | self.view.renderHints().Antialiasing)
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Tamaño inicial de la ventana
        self.setCentralWidget(self.view)
        self.resize(800, 600)

        # (Opcional) Cambiar fondo
        palette = self.view.palette()
        palette.setColor(QPalette.Base, QColor("#f0f0f0"))
        self.view.setPalette(palette)

        # Aquí podrías empezar a dibujar hexágonos
        # Por ahora está vacío
