from dataclasses import dataclass

from entities.common.position import Position


@dataclass
class Column:
    cells: list[Position]
