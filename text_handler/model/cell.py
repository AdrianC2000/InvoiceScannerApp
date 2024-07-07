from dataclasses import dataclass

from entities.common.text_position import TextPosition


@dataclass
class Cell:
    text_positions: list[TextPosition]
