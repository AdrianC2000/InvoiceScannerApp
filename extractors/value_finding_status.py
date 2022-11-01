from enum import Enum


class ValueFindingStatus(Enum):
    FOUND = 1
    VALUE_BELOW = 2
    VALUE_ON_THE_RIGHT = 3
    VALUE_BELOW_OR_ON_THE_RIGHT = 4
    VALUE_MISSING = 5
