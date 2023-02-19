from entities.common.position import Position
from extractors.value_finding_status import ValueFindingStatus


class SearchResponse:

    def __init__(self, key_word: str, value: str, status: ValueFindingStatus, row_position: Position):
        self.__key_word = key_word
        self.__value = value
        self.__status = status
        self.__row_position = row_position

    @property
    def key_word(self) -> str:
        return self.__key_word

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    @property
    def status(self) -> ValueFindingStatus:
        return self.__status

    @status.setter
    def status(self, status: ValueFindingStatus):
        self.__status = status

    @property
    def row_position(self) -> Position:
        return self.__row_position

    @row_position.setter
    def row_position(self, row_position: Position):
        self.__row_position = row_position

    def __repr__(self):
        return '(%r, %r)' % (self.__key_word, self.__value)
