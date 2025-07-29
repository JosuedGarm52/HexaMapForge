from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class CollapsibleSection(QWidget):
    def __init__(self, title, children_data, on_action_callback=None):
        super().__init__()
        self.title = title
        self.children_data = children_data
        self.on_action_callback = on_action_callback

        self.setStyleSheet("""
            QLabel {
                font-weight: bold;
                padding: 4px;
                background-color: #444;
                color: white;
            }
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.header = QLabel(self.title)
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        self.child_buttons = []
        for child in self.children_data:
            btn = QPushButton(child["label"])
            btn.clicked.connect(lambda _, act=child["action"]: self.trigger_action(act))
            btn.setVisible(False)
            self.child_buttons.append(btn)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

        # Mostrar/ocultar al hacer hover
        self.setMouseTracking(True)
        self.header.setMouseTracking(True)
        self.enterEvent = self.show_children
        self.leaveEvent = self.hide_children

    def show_children(self, _):
        for btn in self.child_buttons:
            btn.setVisible(True)

    def hide_children(self, _):
        for btn in self.child_buttons:
            btn.setVisible(False)

    def trigger_action(self, action_name):
        if self.on_action_callback:
            self.on_action_callback(action_name)
