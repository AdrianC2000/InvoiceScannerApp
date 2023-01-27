from entities.common.text_position import TextPosition


class Cell:
    def __init__(self, text_positions: list[TextPosition]):
        self.__text_positions = text_positions

    @property
    def text_positions(self) -> list[TextPosition]:
        return self.__text_positions
