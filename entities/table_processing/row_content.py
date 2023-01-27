class RowContent:
    def __init__(self, cells_content: list[str]):
        self.__cells_content = cells_content

    @property
    def cells_content(self) -> list[str]:
        return self.__cells_content
