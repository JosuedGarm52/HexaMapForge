import os
import json
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontMetrics

from .ToolChild import ToolChild

class ToolHeader(QWidget):
    def __init__(self, title: str, children: List[Dict[str, str]], on_action_callback,
                 parent_bg: str, child_bg: str):
        super().__init__()
        self.on_action_callback = on_action_callback
        self.children_conf = children  # list of dicts with 'label' and 'action'

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {parent_bg}; border-radius:6px;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(0)

        # Header button area
        self.title_btn = QPushButton(title)
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #222;
                font-weight: bold;
                padding: 6px 12px;
            }
            QPushButton:hover {
                color: #000;
            }
        """)
        self.title_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.title_btn)

        # Child container (initially hidden)
        self.child_container = QWidget()
        self.child_layout = QHBoxLayout(self.child_container)
        self.child_layout.setContentsMargins(6, 4, 6, 4)
        self.child_layout.setSpacing(6)
        self.child_container.setVisible(False)
        self.child_container.setStyleSheet(f"background-color: {child_bg}; border-radius:4px;")

        for child in self.children_conf:
            label = child.get("label", "")
            action = child.get("action", label.lower())
            btn = ToolChild(label, action, self.on_action_callback)
            self.child_layout.addWidget(btn)

        self.main_layout.addWidget(self.child_container)

        # Hover events para desplegar hijos
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.child_container.setVisible(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.child_container.setVisible(False)
        return super().leaveEvent(event)

    def sizeHint(self):
        # Ancho estimado según el título y algo de padding
        fm = QFontMetrics(self.font())
        w = fm.horizontalAdvance(self.title_btn.text()) + 30
        return QSize(w, fm.height() + 20)