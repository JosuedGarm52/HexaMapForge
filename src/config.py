# src/config.py
from dataclasses import dataclass

@dataclass
class GridConfig:
    cols: int = 10           # ancho (columnas)
    rows: int = 6            # alto (filas)
    size: int = 30           # radio del hexágono
    orientation: str = "flat"  # "flat" (plano arriba) o "pointy"
    offset: str = "even-q"     # estrategia de offset: "even-q" | "odd-q"
    background: str = "#f0f0f0"