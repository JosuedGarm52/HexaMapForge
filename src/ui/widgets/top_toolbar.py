import os
import json
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QHBoxLayout, QVBoxLayout,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFontMetrics

from .toolbar_section import ToolbarSection

class TopToolbar(QWidget):
    """
    Barra superior gris claro con scroll horizontal y flechas
    que aparecen cuando hay overflow. Carga opcional desde JSON.
    """
    def __init__(self, on_action=None, config_path: str | None = "src/config/toolbar_config.json"):
        super().__init__()
        self.on_action = on_action or (lambda name: None)

        # Altura reservada y color de fondo
        self.setFixedHeight(72)
        self.setStyleSheet("background-color: #f0f0f0;")  # fondo gris claro para toda la barra
        self.setContentsMargins(0, 0, 0, 0)

        # Flechas de desplazamiento
        self.left_btn = QPushButton("◀")
        self.right_btn = QPushButton("▶")
        for b in (self.left_btn, self.right_btn):
            b.setFixedWidth(28)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #555;
                    border: none;
                    font-weight: bold;
                }
                QPushButton:hover { color: #222; }
            """)
        self.left_btn.clicked.connect(lambda: self._scroll(-1))
        self.right_btn.clicked.connect(lambda: self._scroll(+1))

        # Área desplazable
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)

        # Contenido interno
        self.inner = QWidget()
        self.inner_layout = QHBoxLayout(self.inner)
        self.inner_layout.setContentsMargins(10, 6, 10, 6)
        self.inner_layout.setSpacing(12)
        self.scroll.setWidget(self.inner)

        # Layout principal: [◀][scroll][▶]
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(4)
        main_layout.addWidget(self.left_btn)
        main_layout.addWidget(self.scroll, 1)
        main_layout.addWidget(self.right_btn)
        self.setLayout(main_layout)

        # Cargar configuración si existe
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                for section in config:
                    title = section.get("title", "Sección")
                    children = [c.get("label", "") for c in section.get("children", [])]
                    actions = {c.get("label", ""): c.get("action", "").strip() for c in section.get("children", [])}
                    self.add_section(title, children, actions)
            except Exception as e:
                print(f"[Toolbar] Error leyendo {config_path}: {e}")

        # Ocultar flechas si no hay overflow al inicio
        self._update_arrow_visibility()

        # Monitorear cambios de tamaño del contenido
        self.inner.installEventFilter(self)

    def add_section(self, title: str, children: list[str], actions: dict[str, str] | None = None):
        section = ToolbarSection(title, children, self.on_action, actions)
        self.inner_layout.addWidget(section)
        self._update_arrow_visibility()

    # ---- Desplazamiento y flechas ----
    def _scroll(self, direction: int):
        step = 140  # px por “clic” de flecha
        bar = self.scroll.horizontalScrollBar()
        bar.setValue(bar.value() + direction * step)

    def _update_arrow_visibility(self):
        # Mostrar flechas solo si el contenido desborda el viewport
        overflow = self.inner.sizeHint().width() > self.scroll.viewport().width()
        self.left_btn.setVisible(overflow)
        self.right_btn.setVisible(overflow)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_arrow_visibility()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_arrow_visibility()

    def eventFilter(self, obj, event):
        if obj is self.inner and event.type() in (QEvent.Resize,):
            self._update_arrow_visibility()
        return super().eventFilter(obj, event)
