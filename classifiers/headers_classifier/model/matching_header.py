from dataclasses import dataclass

from entities.table_processing.confidence_calculation import ConfidenceCalculation


@dataclass
class MatchingHeader:
    phrase: str
    confidence_calculation: ConfidenceCalculation
    column_index: int
