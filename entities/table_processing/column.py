from entities.common.position import Position


class Column:
    def __init__(self, cells: list[Position]):
        self.__cells = cells

    @property
    def cells(self) -> list[Position]:
        return self.__cells
