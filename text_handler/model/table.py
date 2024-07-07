from dataclasses import dataclass

from text_handler.model.row import Row


@dataclass
class Table:
    rows: list[Row]
