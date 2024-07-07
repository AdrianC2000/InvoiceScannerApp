from dataclasses import dataclass

from entities.common.position import Position
from extractors.value_finding_status import ValueFindingStatus


@dataclass
class SearchResponse:
    key_word: str
    value: str
    status: ValueFindingStatus
    row_position: Position
