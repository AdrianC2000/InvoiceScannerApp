from dataclasses import dataclass

from columns_separator.model.line_property import LineProperty


@dataclass
class Line:
    lines_properties: list[LineProperty]
