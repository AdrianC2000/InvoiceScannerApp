from entities.common.position import Position
from entities.common.text_position import TextPosition


class BlockPosition:

    def __init__(self, position: Position, rows: list[TextPosition]):
        self.__position = position
        self.__rows = rows

    @property
    def position(self) -> Position:
        return self.__position

    @property
    def rows(self) -> list[TextPosition]:
        return self.__rows

    @rows.setter
    def rows(self, rows: list[TextPosition]):
        self.__rows = rows
