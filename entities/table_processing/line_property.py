from numpy import ndarray


class LineProperty:
    def __init__(self, index: int, image_row: ndarray):
        self.__index = index
        self.__line = image_row

    @property
    def index(self) -> int:
        return self.__index

    @property
    def image_row(self) -> ndarray:
        return self.__line
