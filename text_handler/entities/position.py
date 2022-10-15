class Position:

    def __init__(self, starting_x: int, starting_y: int, ending_x: int, ending_y: int):
        self.__starting_x = starting_x
        self.__starting_y = starting_y
        self.__ending_x = ending_x
        self.__ending_y = ending_y

    @property
    def starting_x(self) -> int:
        return self.__starting_x

    @property
    def starting_y(self) -> int:
        return self.__starting_y

    @property
    def ending_x(self) -> int:
        return self.__ending_x

    @property
    def ending_y(self) -> int:
        return self.__ending_y



