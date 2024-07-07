from dataclasses import dataclass

from columns_seperator.model.line import Line


@dataclass
class TableLines:
    lines: list[Line]
