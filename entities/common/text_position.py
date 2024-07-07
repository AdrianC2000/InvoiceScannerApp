from dataclasses import dataclass

from entities.common.position import Position


@dataclass
class TextPosition:
    text: str
    position: Position

    def __lt__(self, other):
        return self.position.starting_x < other.position.starting_x

    def __repr__(self):
        return '["' + self.text + '"' + " -> " + str(self.position.starting_x) + ", " \
            + str(self.position.starting_y) + ", " + str(self.position.ending_x) + ", " \
            + str(self.position.ending_y) + "]"
