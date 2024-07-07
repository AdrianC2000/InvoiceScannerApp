from dataclasses import dataclass
from typing import List


@dataclass
class HeaderPatterns:
    header_name: str
    patterns_set: List[str]
