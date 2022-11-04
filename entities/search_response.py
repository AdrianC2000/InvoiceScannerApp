from extractors.value_finding_status import ValueFindingStatus


class SearchResponse:

    def __init__(self, key_word: str, value: str, status: ValueFindingStatus):
        self.__key_word = key_word
        self.__value = value
        self.__status = status

    @property
    def key_word(self) -> str:
        return self.__key_word

    @property
    def value(self) -> str:
        return self.__value

    @property
    def status(self) -> ValueFindingStatus:
        return self.__status
