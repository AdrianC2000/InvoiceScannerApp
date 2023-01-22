from numpy import ndarray
from entities.position import Position


class TablePosition:

    def __init__(self, table: ndarray, position: Position):
        self.__table = table
        self.__position = position

    @property
    def table(self) -> ndarray:
        return self.__table

    @property
    def position(self) -> Position:
        return self.__position
