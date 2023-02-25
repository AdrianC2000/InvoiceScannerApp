from entities.table_processing.confidence_calculation import ConfidenceCalculation
from entities.key_data_processing.block_position import BlockPosition


class MatchingBlock:

    def __init__(self, block: BlockPosition, confidence_calculation: ConfidenceCalculation, row_index: int,
                 last_word_index: int):
        self.__block = block
        self.__confidence_calculation = confidence_calculation
        self.__row_index = row_index
        self.__last_word_index = last_word_index

    @property
    def block(self) -> BlockPosition:
        return self.__block

    @block.setter
    def block(self, block: BlockPosition):
        self.__block = block

    @property
    def confidence_calculation(self) -> ConfidenceCalculation:
        return self.__confidence_calculation

    @property
    def row_index(self) -> int:
        return self.__row_index

    @property
    def last_word_index(self) -> int:
        return self.__last_word_index
