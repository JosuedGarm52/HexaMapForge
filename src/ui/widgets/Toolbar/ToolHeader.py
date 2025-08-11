import os
import json
from typing import List, Dict
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QPushButton, QMenu, QSizePolicy
from PySide6.QtGui import QAction, QFontMetrics

from .ToolChild import ToolChild  # No se usa aquí pero lo dejo si lo usas en otro lado

class ToolHeader(QWidget):
    def __init__(self, title: str, children: List[Dict[str, str]], on_action_callback,
                 parent_bg: str, child_bg: str):
        super().__init__()
        self.on_action_callback = on_action_callback
        self.children_conf = children  # list of dicts with 'label' and 'action'

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {parent_bg}; border-radius:6px;")

        # Botón principal
        self.title_btn = QPushButton(title, self)
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: #222;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                color: #000;
                background-color: {child_bg};
            }}
        """)
        self.title_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Crear menú
        self.menu = QMenu(self.title_btn)
        self.menu.setStyleSheet(f"""
            QMenu {{
                background-color: {child_bg};
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 12px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: #ccc;
            }}
        """)

        for child in self.children_conf:
            label = child.get("label", "")
            action_name = child.get("action", label.lower())
            action = QAction(label, self.menu)
            action.triggered.connect(lambda checked, a=action_name: self.on_action_callback(a))
            self.menu.addAction(action)

        self.title_btn.clicked.connect(self.show_menu)

    def show_menu(self):
        # Mostrar menú justo debajo del botón
        pos = self.title_btn.mapToGlobal(self.title_btn.rect().bottomLeft())
        self.menu.exec(pos)

    def sizeHint(self):
        # Ancho estimado según el título y algo de padding
        fm = QFontMetrics(self.font())
        w = fm.horizontalAdvance(self.title_btn.text()) + 30
        return QSize(w, fm.height() + 20)