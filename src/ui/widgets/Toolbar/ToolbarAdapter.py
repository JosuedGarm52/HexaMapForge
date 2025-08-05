import os
import json
from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
)
from PySide6.QtCore import Qt

from .ToolHeader import ToolHeader

class ToolbarAdapter(QWidget):
    def __init__(self,
                 headers: List[ToolHeader],
                 on_action_callback,
                 max_visible: Optional[int] = None,
                 orientation: str = "horizontal"):
        super().__init__()
        self.on_action_callback = on_action_callback
        self.orientation = orientation  # "horizontal" o "vertical"
        self.max_visible = max_visible  # si None, se calcula por espacio
        self.headers: List[ToolHeader] = headers
        self.visible_start = 0

        self.left_btn = QPushButton("◀")
        self.right_btn = QPushButton("▶")
        for b in (self.left_btn, self.right_btn):
            b.setFixedWidth(28)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    font-weight: bold;
                    color: #444;
                }
                QPushButton:hover { color: #222; }
            """)

        self.left_btn.clicked.connect(self._shift_left)
        self.right_btn.clicked.connect(self._shift_right)

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

    def _available_slots(self):
        if self.max_visible is not None:
            return self.max_visible
        # calcular por espacio visible (simplificado: contar cuántos caben)
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

        # actualizar flechas
        self.left_btn.setVisible(self.visible_start > 0)
        self.right_btn.setVisible(end < len(self.headers))

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