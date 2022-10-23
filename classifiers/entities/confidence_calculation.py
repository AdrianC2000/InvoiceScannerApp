class ConfidenceCalculation:

    def __init__(self, value: str, confidence: float):
        self.__value = value
        self.__confidence = confidence

    @property
    def value(self) -> str:
        return self.__value

    @property
    def confidence(self) -> float:
        return self.__confidence
