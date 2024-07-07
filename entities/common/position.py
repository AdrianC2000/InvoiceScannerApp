from dataclasses import dataclass


@dataclass
class Position:
    starting_x: int
    starting_y: int
    ending_x: int
    ending_y: int

    def __eq__(self, other):
        if isinstance(other, Position):
            return (self.starting_x == other.starting_x and
                    self.starting_y == other.starting_y and
                    self.ending_x == other.ending_x and
                    self.ending_y == other.ending_y)
        return False
