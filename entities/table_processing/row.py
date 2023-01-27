from entities.table_processing.cell import Cell


class Row:
    def __init__(self, cells: list[Cell]):
        self.__cells = cells

    @property
    def cells(self) -> list[Cell]:
        return self.__cells
