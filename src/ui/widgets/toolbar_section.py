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
        # Fondo del contenedor padre (gris claro, sin borde)
        self.setStyleSheet("background-color: #e0e0e0; border: none;")
        self.setMouseTracking(True)

        # Layout vertical: título + hijos
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Barra título padre (barra completa gris más oscuro)
        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #b0b0b0;")  # gris más oscuro
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(10, 4, 10, 4)  # padding horizontal y vertical
        self.title_bar_layout.setSpacing(0)

        # Hijos (invisibles por defecto)
        self.title_btn = QPushButton(title)
        self.title_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #222;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                color: #000;
            }
        """)
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.setFixedHeight(self._calc_height(title))
        self.title_bar_layout.addWidget(self.title_btn)
        self.layout.addWidget(self.title_bar)

        # Botones hijos con borde cuadrado y fondo blanco, dentro de la barra padre
        self.child_buttons = []
        for label in children:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #999999;
                    padding: 4px 12px;
                    margin: 4px 10px;  /* margen para separarlo de los bordes y título */
                    border-radius: 2px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
            """)
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