from dataclasses import dataclass

from text_handler.model.cell import Cell


@dataclass
class Row:
    cells: list[Cell]
