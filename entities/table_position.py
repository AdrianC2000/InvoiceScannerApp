from numpy import ndarray
from entities.position import Position


class TablePosition:

    def __init__(self, table_image: ndarray, position: Position):
        self.__table = table_image
        self.__position = position

    @property
    def table_image(self) -> ndarray:
        return self.__table

    @property
    def position(self) -> Position:
        return self.__position
