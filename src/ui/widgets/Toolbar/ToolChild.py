import os
import json
from typing import List, Optional, Dict
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QSize, Signal, QEvent
from PySide6.QtGui import QFontMetrics


class ToolChild(QPushButton):
    def __init__(self, label: str, action: str, on_action_callback):
        super().__init__(label)
        self.action = action
        self.on_action_callback = on_action_callback
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #888;
                padding: 4px 12px;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.clicked.connect(self._trigger)

    def _trigger(self):
        if self.on_action_callback:
            self.on_action_callback(self.action)
