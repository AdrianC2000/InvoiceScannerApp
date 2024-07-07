from dataclasses import dataclass
from typing import List

from classifiers.headers_classifier.model.header_patterns import HeaderPatterns


@dataclass
class TableHeadersPatterns:
    headers_patterns: List[HeaderPatterns]

    def remove_header_pattern(self, column_name: str):
        self.headers_patterns = [header for header in self.headers_patterns
                                 if header.header_name != column_name]
