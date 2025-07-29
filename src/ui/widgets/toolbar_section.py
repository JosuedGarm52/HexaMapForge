


from PySide6.QtWidgets import QWidget, QPushButton, QScrollArea, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFontMetrics
import os
import json

class ToolbarSection(QWidget):
    """
    Sección padre con botones hijos que aparecen al hacer hover.
    """
    def __init__(self, title: str, children: list[str], on_action, actions: dict[str, str] | None = None):
        super().__init__()
        self.on_action = on_action
        self.actions = actions or {}

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #cccccc; border-radius: 6px;")
        self.setMouseTracking(True)

        # Layout vertical: título + hijos
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(4)

        # Botón padre (centrado, alto según texto + padding)
        self.title_btn = QPushButton(title)
        self.title_btn.setStyleSheet(self._style_parent_btn())
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.setFixedHeight(self._calc_height(title))
        self.layout.addWidget(self.title_btn)

        # Hijos (invisibles por defecto)
        self.child_buttons = []
        for label in children:
            btn = QPushButton(label)
            btn.setStyleSheet(self._style_child_btn())
            btn.setCursor(Qt.PointingHandCursor)
            btn.setVisible(False)
            action = self.actions.get(label, label.lower())
            btn.clicked.connect(lambda _, name=action: self.on_action(name))
            self.layout.addWidget(btn)
            self.child_buttons.append(btn)

    # ----- Hover en toda la sección (no solo en el botón) -----
    def enterEvent(self, event):
        for b in self.child_buttons:
            b.setVisible(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        for b in self.child_buttons:
            b.setVisible(False)
        return super().leaveEvent(event)

    # ----- Estilos y utilidades -----
    def _calc_height(self, text) -> int:
        fm = QFontMetrics(self.font())
        return fm.height() + 10  # 5px de margen arriba/abajo

    def _style_parent_btn(self) -> str:
        return """
        QPushButton {
            background-color: #aaaaaa;
            color: #222;
            padding: 4px 14px;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            qproperty-iconSize: 16px;
        }
        QPushButton:hover {
            background-color: #999999;
        }
        """

    def _style_child_btn(self) -> str:
        return """
        QPushButton {
            background-color: #dddddd;
            color: #333;
            padding: 3px 10px;
            font-size: 12px;
            border: none;
            border-radius: 3px;
            text-align: left;
        }
        QPushButton:hover {
            background-color: #bbbbbb;
        }
        """