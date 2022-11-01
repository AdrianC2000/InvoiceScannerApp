from classifiers.entities.confidence_calculation import ConfidenceCalculation
from text_handler.entities.block_position import BlockPosition


class MatchingBlock:

    def __init__(self, block: BlockPosition, confidence_calculation: ConfidenceCalculation, row_index: int,
                 patterns_set_index: int):
        self.__block = block
        self.__confidence_calculation = confidence_calculation
        self.__row_index = row_index
        self.__patterns_set_index = patterns_set_index

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
    def patterns_set_index(self) -> int:
        return self.__patterns_set_index
