from entities.table_processing.line import Line


class TableLines:
    def __init__(self, lines: list[Line]):
        self.__lines = lines

    @property
    def lines(self) -> list[Line]:
        return self.__lines
