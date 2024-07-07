from dataclasses import dataclass
from typing import List

from classifiers.headers_classifier.model.matching_header import MatchingHeader


@dataclass
class MatchingHeaders:
    headers: List[MatchingHeader]

    def get_by_column_index(self, column_index: int) -> MatchingHeader | None:
        try:
            return next(header for header in self.headers if header.column_index == column_index)
        except StopIteration:
            return None
