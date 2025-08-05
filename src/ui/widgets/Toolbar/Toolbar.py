import os
import json
from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout
)
from PySide6.QtCore import Qt


from .ToolHeader import ToolHeader
from .ToolbarAdapter import ToolbarAdapter

class Toolbar(QWidget):
    def __init__(self,
                 config_path: str,
                 on_action_callback,
                 background_color: str = "#f0f0f0",
                 header_bg: str = "#aaaaaa",
                 child_bg: str = "#e8e8e8",
                 **adapter_kwargs):
        super().__init__()
        self.on_action_callback = on_action_callback
        self.header_bg = header_bg
        self.child_bg = child_bg
        self.background_color = background_color

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {self.background_color};")
        self.setFixedHeight(72)

        self.headers: List[ToolHeader] = []
        self.adapter: Optional[ToolbarAdapter] = None

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(4)

        self.setLayout(self.main_layout)

        self._load_config(config_path)
        self.adapter = ToolbarAdapter(self.headers, self.on_action_callback, **adapter_kwargs)
        self.main_layout.addWidget(self.adapter)

    def _load_config(self, path):
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"[Toolbar] no se pudo cargar {path}: {e}")
            return

        for section in config:
            title = section.get("title", "Sección")
            children = section.get("children", [])
            th = ToolHeader(title, children, self.on_action_callback, self.header_bg, self.child_bg)
            self.headers.append(th)