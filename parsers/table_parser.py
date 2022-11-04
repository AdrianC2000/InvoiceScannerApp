import json

from entities.matching_header import MatchingHeader
from parsers.json_encoder import JsonEncoder
from entities.table_item import TableItem


def save_to_file(table_items: list[TableItem]):
    table_json = json.dumps(table_items, indent=4, cls=JsonEncoder, ensure_ascii=False)
    f = open("resources/entire_flow/10.Final table.json", mode="w", encoding="utf-8")
    f.write(table_json)
    f.close()


class TableParser:

    def __init__(self, matching_headers: list[MatchingHeader], rows: list[list[str]]):
        self.__matching_headers = matching_headers
        self.__rows = rows

    def parse_rows(self) -> list[TableItem]:
        table_items = list()
        for row in self.__rows:
            row_dict = self.parse_row(row)
            table_items.append(TableItem(row_dict))
        save_to_file(table_items)
        return table_items

    def parse_row(self, row: list[str]) -> dict[str, str]:
        row_dict = {}
        for index, cell_phrase in enumerate(row):
            row_dict[self.__matching_headers[index].confidence_calculation.value] = cell_phrase
        return row_dict
