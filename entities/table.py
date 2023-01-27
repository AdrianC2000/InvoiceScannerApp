from entities.cell import Cell
from entities.row import Row


class Table:
    def __init__(self, rows: list[Row]):
        self.__rows = rows

    @property
    def rows(self) -> list[Row]:
        return self.__rows
