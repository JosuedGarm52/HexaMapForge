from src.core.hex_tile import HexTile


class MapGenerator:
    def __init__(self, rows, cols, tile_size=30):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size

    def generate(self):
        tiles = []
        for r in range(self.rows):
            # En filas impares, desplazamos una columna menos para la forma “zigzag”
            num_cols = self.cols if r % 2 == 0 else self.cols - 1

            for q in range(num_cols):
                # La fórmula para q y r con offset horizontal en hex axial coords
                hex_q = q - (r // 2)
                hex_r = r
                tile = HexTile(hex_q, hex_r, size=self.tile_size)
                tiles.append(tile)
        return tiles

