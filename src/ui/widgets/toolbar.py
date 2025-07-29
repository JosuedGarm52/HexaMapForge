import json
from PySide6.QtWidgets import QWidget, QHBoxLayout
from src.ui.widgets.collapsible_section import CollapsibleSection


class TopToolbar(QWidget):
    def __init__(self, config_path="src/config/toolbar_config.json", on_action=None):
        super().__init__()
        self.setStyleSheet("background-color: #333;")
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)

        with open(config_path, "r") as f:
            config = json.load(f)

        for section in config:
            widget = CollapsibleSection(
                section["title"],
                section["children"],
                on_action_callback=on_action
            )
            self.layout.addWidget(widget)
