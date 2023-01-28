from entities.table_processing.line_property import LineProperty


class Line:
    def __init__(self, lines_properties: list[LineProperty]):
        self.__lines_properties = lines_properties

    @property
    def lines_properties(self) -> list[LineProperty]:
        return self.__lines_properties
