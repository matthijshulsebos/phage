from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def moved(self, dx: int, dy: int) -> "Coord":
        return Coord(self.x + dx, self.y + dy)

    def neighbors4(self, board_size) -> List["Coord"]:
        if self.x < 0 or self.x >= board_size or self.y < 0 or self.y >= board_size:
            raise ValueError("Coordinate out of board bounds.")
        else:
            neighbors = []
            if self.x > 0:
                # Up
                neighbors.append(Coord(self.x - 1, self.y))
            if self.x < board_size - 1:
                # Down
                neighbors.append(Coord(self.x + 1, self.y))
            if self.y > 0:
                # Left
                neighbors.append(Coord(self.x, self.y - 1))
            if self.y < board_size - 1:
                # Right
                neighbors.append(Coord(self.x, self.y + 1))

            return neighbors
