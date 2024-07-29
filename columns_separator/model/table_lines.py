from dataclasses import dataclass

from columns_separator.model.line import Line


@dataclass
class TableLines:
    lines: list[Line]
