import json

from entities.matching_header import MatchingHeader
from entities.parsed_table import ParsedTable
from entities.row_content import RowContent
from parsers.json_encoder import JsonEncoder
from entities.table_item import TableProduct
from settings.config_consts import ConfigConsts

__FINAL_TABLE_OUTPUT_PATH_PREFIX = "9.Final table.json"


def save_to_file(table_items: list[TableProduct]):
    table_json = json.dumps(table_items, indent=4, cls=JsonEncoder, ensure_ascii=False)
    f = open(ConfigConsts.DIRECTORY_TO_SAVE + __FINAL_TABLE_OUTPUT_PATH_PREFIX, mode="w", encoding="utf-8")
    f.write(table_json)
    f.close()


class TableParser:

    def __init__(self, matching_headers: list[MatchingHeader], rows_content: list[RowContent]):
        self.__matching_headers = matching_headers
        self.__rows_content = rows_content

    def get_table_content(self) -> ParsedTable:
        table_items = list()
        for row in self.__rows_content:
            row_dict = self.parse_row(row.cells_content)
            table_items.append(TableProduct(row_dict))
        save_to_file(table_items[1:len(table_items)])
        return ParsedTable(table_items[1:len(table_items)])

    def parse_row(self, row: list[str]) -> dict[str, str]:
        row_dict = {}
        for index, cell_phrase in enumerate(row):
            row_dict[self.__matching_headers[index].confidence_calculation.value] = cell_phrase
        return row_dict
