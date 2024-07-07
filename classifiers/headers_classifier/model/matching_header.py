from dataclasses import dataclass

from classifiers.headers_classifier.model.confidence_calculation import ConfidenceCalculation


@dataclass
class MatchingHeader:
    phrase: str
    confidence_calculation: ConfidenceCalculation
    column_index: int
