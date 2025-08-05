import os
import json
from typing import List, Optional
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from .ToolHeader import ToolHeader


class ToolbarAdapter(QWidget):
    def __init__(
        self,
        headers: List[ToolHeader],
        on_action_callback,
        max_visible: Optional[int] = None,
        orientation: str = "horizontal"
    ):
        super().__init__()
        self.on_action_callback = on_action_callback
        self.orientation = orientation  # "horizontal" o "vertical"
        self.max_visible = max_visible  # si None, se calcula por espacio
        self.headers: List[ToolHeader] = headers
        self.visible_start = 0

        # Flechas con SVG / fallback
        self.left_btn = self._make_arrow_button("left")
        self.right_btn = self._make_arrow_button("right")
        self.left_btn.clicked.connect(self._shift_left)
        self.right_btn.clicked.connect(self._shift_right)

        # Contenedor de headers
        if self.orientation == "horizontal":
            self.container = QWidget()
            self.container_layout = QHBoxLayout(self.container)
            self.container_layout.setContentsMargins(0, 0, 0, 0)
            self.container_layout.setSpacing(8)
            main = QHBoxLayout(self)
        else:
            self.container = QWidget()
            self.container_layout = QVBoxLayout(self.container)
            self.container_layout.setContentsMargins(0, 0, 0, 0)
            self.container_layout.setSpacing(8)
            main = QVBoxLayout(self)

        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(4)
        main.addWidget(self.left_btn)
        main.addWidget(self.container, 1)
        main.addWidget(self.right_btn)
        self.setLayout(main)

        self._relayout()

    def _make_arrow_button(self, direction: str) -> QPushButton:
        btn = QPushButton()
        btn.setFixedSize(28, 28)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFlat(True)

        # Resolver ruta al repo root y a los SVG
        repo_root = Path(__file__).resolve().parents[4]  # debería llegar a HexaMapForge/
        icons_dir = repo_root / "assets" / "icons"
        svg_name = "arrow-left.svg" if direction == "left" else "arrow-right.svg"
        svg_path = icons_dir / svg_name

        # DEBUG: imprimir ruta y existencia (puedes quitar después)
        print(f"[ToolbarAdapter] buscando icono {svg_name} en: {svg_path} (existe={svg_path.exists()})")

        if svg_path.exists():
            icon = QIcon(str(svg_path))
            btn.setIcon(icon)
            btn.setIconSize(QSize(16, 16))
        else:
            # fallback de texto
            btn.setText("◀" if direction == "left" else "▶")
            btn.setStyleSheet("font-weight:bold; color:#444;")

        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(0,0,0,0.05);
                border-radius: 4px;
            }
            QPushButton:disabled {
                color: #aaa;
            }
        """)
        return btn

    def _available_slots(self):
        if self.max_visible is not None:
            return self.max_visible
        # calcular por espacio visible
        if self.orientation == "horizontal":
            width = self.container.width()
            count = 0
            total = 0
            for h in self.headers[self.visible_start:]:
                w = h.sizeHint().width() + 8
                if total + w > width:
                    break
                total += w
                count += 1
            return max(1, count)
        else:
            # vertical: mostrar todos o limitar por max_visible
            return self.max_visible or len(self.headers)

    def _relayout(self):
        # limpiar
        for i in reversed(range(self.container_layout.count())):
            item = self.container_layout.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    self.container_layout.removeWidget(w)
                    w.setParent(None)

        slots = self._available_slots()
        end = min(len(self.headers), self.visible_start + slots)
        for header in self.headers[self.visible_start:end]:
            self.container_layout.addWidget(header)

        # actualizar flechas: visibilidad y habilitación
        self.left_btn.setVisible(self.visible_start > 0)
        self.right_btn.setVisible(end < len(self.headers))
        self.left_btn.setEnabled(self.visible_start > 0)
        self.right_btn.setEnabled(end < len(self.headers))

    def _shift_left(self):
        if self.visible_start > 0:
            self.visible_start -= 1
            self._relayout()

    def _shift_right(self):
        if self.visible_start < len(self.headers) - 1:
            self.visible_start += 1
            self._relayout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._relayout()