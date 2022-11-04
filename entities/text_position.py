from entities.position import Position


class TextPosition:

    def __init__(self, text: str, position: Position):
        self.__text = text
        self.__position = position

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def position(self) -> Position:
        return self.__position

    def __lt__(self, other):
        return self.__position.starting_x < other.position.starting_x

    def __repr__(self):
        return '["' + self.__text + '"' + " -> " + str(self.__position.starting_x) + ", " \
               + str(self.__position.starting_y) + ", " + str(self.__position.ending_x) + ", " \
               + str(self.__position.ending_y) + "]"
