from dataclasses import dataclass
from typing import List


@dataclass
class RowContent:
    cells_content: List[str]
