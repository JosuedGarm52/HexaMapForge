# src/core/hex_grid.py
from typing import Dict, Tuple, Iterable
from PySide6.QtWidgets import QGraphicsScene
from src.core.hex_tile import HexTile
from src.config import GridConfig

# Desplazamientos de vecinos en axial (q, r) para orientación plana
NEIGHBOR_DIRS: Iterable[Tuple[int, int]] = [
    (+1, 0), (+1, -1), (0, -1),
    (-1, 0), (-1, +1), (0, +1),
]

class HexGrid:
    """
    Genera y administra un mapa rectangular de hexágonos usando axial coords (q, r).
    Para grillas rectangulares, usamos layout "even-q" (columnas desplazadas).
    """
    def __init__(self, config: GridConfig):
        self.config = config
        self.tiles: Dict[Tuple[int, int], HexTile] = {}  # key: (q, r)

    def build(self):
        cols = self.config.cols
        rows = self.config.rows
        size = self.config.size

        # Rectángulo con orientación "flat" y offset "even-q"
        for col in range(cols):
            for row in range(rows):
                if self.config.offset == "even-q":
                    r = row - (col // 2)
                else:  # "odd-q"
                    r = row - ((col + 1) // 2)
                q = col

                tile = HexTile(q, r, size=size)
                self.tiles[(q, r)] = tile

        return self

    def add_to_scene(self, scene: QGraphicsScene):
        for tile in self.tiles.values():
            scene.addItem(tile)

    def get_tile(self, q: int, r: int) -> HexTile | None:
        return self.tiles.get((q, r))

    def neighbors(self, q: int, r: int):
        for dq, dr in NEIGHBOR_DIRS:
            t = self.get_tile(q + dq, r + dr)
            if t:
                yield t

    # --------- Persistencia básica (demo) ----------
    def to_dict(self):
        return {
            "config": {
                "cols": self.config.cols,
                "rows": self.config.rows,
                "size": self.config.size,
                "orientation": self.config.orientation,
                "offset": self.config.offset,
                "background": self.config.background,
            },
            "tiles": [
                {"q": t.q, "r": t.r, "color": t.color.name()}
                for t in self.tiles.values()
            ]
        }

    @classmethod
    def from_dict(cls, data: dict):
        cfg_dict = data["config"]
        cfg = GridConfig(**cfg_dict)
        grid = cls(cfg)
        for tdata in data["tiles"]:
            tile = HexTile(tdata["q"], tdata["r"], size=cfg.size, color=tdata["color"])
            grid.tiles[(tile.q, tile.r)] = tile
        return grid
