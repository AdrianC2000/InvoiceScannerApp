from entities.key_data_processing.block_position import BlockPosition


class MatchingBlock:

    def __init__(self, block: BlockPosition, key_word: str, row_index: int, last_word_index: int):
        self.__block = block
        self.__key_word = key_word
        self.__row_index = row_index
        self.__last_word_index = last_word_index

    @property
    def block(self) -> BlockPosition:
        return self.__block

    @block.setter
    def block(self, block: BlockPosition):
        self.__block = block

    @property
    def key_word(self) -> str:
        return self.__key_word

    @property
    def row_index(self) -> int:
        return self.__row_index

    @property
    def last_word_index(self) -> int:
        return self.__last_word_index
