from classifiers.entities.confidence_calculation import ConfidenceCalculation
from text_handler.entities.block_position import BlockPosition


class MatchingBlock:

    def __init__(self, block: BlockPosition, confidence_calculation: ConfidenceCalculation, row_index: int):
        self.__block = block
        self.__confidence_calculation = confidence_calculation
        self.__row_index = row_index

    @property
    def block(self) -> BlockPosition:
        return self.__block

    @property
    def confidence_calculation(self) -> ConfidenceCalculation:
        return self.__confidence_calculation

    @property
    def row_index(self) -> int:
        return self.__row_index
