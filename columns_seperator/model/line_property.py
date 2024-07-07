from dataclasses import dataclass

from numpy import ndarray


@dataclass
class LineProperty:
    index: int
    image_row: ndarray
