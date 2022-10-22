from classifiers.entities.confidence_calculation import ConfidenceCalculation


class MatchingHeader:

    def __init__(self, phrase: str, confidence_calculation: ConfidenceCalculation):
        self.__phrase = phrase
        self.__confidence_calculation = confidence_calculation

    @property
    def phrase(self) -> str:
        return self.__phrase

    @property
    def confidence_calculation(self) -> ConfidenceCalculation:
        return self.__confidence_calculation



