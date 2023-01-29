import json

from entities.table_processing.matching_header import MatchingHeader
from entities.table_processing.parsed_table import ParsedTable
from entities.table_processing.row_content import RowContent
from parsers.json_encoder import JsonEncoder
from entities.table_processing.table_item import TableProduct
from settings.config_consts import ConfigConsts


class TableParser:

    __FINAL_TABLE_OUTPUT_PATH_PREFIX = "9.Final table.json"

    def __init__(self, matching_headers: list[MatchingHeader], rows_content: list[RowContent]):
        self.__matching_headers = matching_headers
        self.__rows_content = rows_content

    def get_table_content(self) -> ParsedTable:
        table_items = list()
        for row in self.__rows_content:
            row_dict = self._parse_row(row.cells_content)
            table_items.append(TableProduct(row_dict))
        self._save_to_file(table_items[1:len(table_items)])
        return ParsedTable(table_items[1:len(table_items)])

    def _parse_row(self, row: list[str]) -> dict[str, str]:
        row_dict = dict()
        for index, cell_phrase in enumerate(row):
            row_dict[self.__matching_headers[index].confidence_calculation.value] = cell_phrase
        return row_dict

    def _save_to_file(self, table_items: list[TableProduct]):
        table_json = json.dumps(table_items, indent=4, cls=JsonEncoder, ensure_ascii=False)
        with open(ConfigConsts.DIRECTORY_TO_SAVE + self.__FINAL_TABLE_OUTPUT_PATH_PREFIX,
                  mode="w", encoding="utf-8") as f:
            f.write(table_json)
