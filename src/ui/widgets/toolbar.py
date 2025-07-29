from PySide6.QtWidgets import (
    QWidget, QScrollArea, QHBoxLayout, QPushButton, QFrame,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontMetrics


class TopToolbar(QWidget):
    def __init__(self, on_action=None):
        super().__init__()
        self.on_action = on_action or (lambda name: None)

        self.setFixedHeight(50)  # Altura mínima reservada
        self.setContentsMargins(0, 0, 0, 0)

        # Área de scroll horizontal
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        # Contenido interno
        self.inner_widget = QWidget()
        self.inner_layout = QHBoxLayout(self.inner_widget)
        self.inner_layout.setContentsMargins(5, 5, 5, 5)
        self.inner_layout.setSpacing(10)
        self.scroll_area.setWidget(self.inner_widget)

        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        # Espaciador al final para mantener centrado o margen
        self.inner_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

    def add_section(self, name: str, action: str = None):
        """Agrega un botón como sección padre."""
        btn = QPushButton(name)
        btn.setCheckable(False)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(self._calculate_button_height(name))
        btn.setStyleSheet(self._button_style())

        btn.clicked.connect(lambda: self.on_action(action or name.lower()))
        self.inner_layout.insertWidget(self.inner_layout.count() - 1, btn)

    def _calculate_button_height(self, text):
        """Calcula una altura ajustada al texto con algo de padding."""
        font_metrics = QFontMetrics(self.font())
        text_height = font_metrics.height()
        return text_height + 10  # 5px arriba y abajo

    def _button_style(self):
        return """
        QPushButton {
            background-color: #dddddd;
            color: #333333;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #bbbbbb;
        }
        """
