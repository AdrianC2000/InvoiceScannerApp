import json

from classifiers.headers_classifier.model.matching_header import MatchingHeader
from classifiers.headers_classifier.model.matching_headers import MatchingHeaders
from entities.table_processing.parsed_table import ParsedTable
from entities.table_processing.row_content import RowContent
from invoice_processing_utils.parsers.json_encoder import JsonEncoder
from entities.table_processing.table_item import TableProduct
from settings.config_consts import ConfigConsts


class TableParser:

    __FINAL_TABLE_OUTPUT_PATH_PREFIX = "9.Final table.json"

    def __init__(self, matching_headers: MatchingHeaders, rows_content: list[RowContent]):
        self.__matching_headers = matching_headers
        self.__rows_content = rows_content

    def get_table_content(self) -> ParsedTable:
        table_items = list()
        for row in self.__rows_content:
            table_product = self._parse_row_to_table_product(row.cells_content)
            table_items.append(table_product)
        self._save_to_file(table_items[1:len(table_items)])
        return ParsedTable(table_items[1:len(table_items)])

    def _parse_row_to_table_product(self, row: list[str]) -> TableProduct:
        row_dict = dict()
        for index, cell_phrase in enumerate(row):
            matching_header = self.__matching_headers.get_by_column_index(index)
            if matching_header:
                row_dict[matching_header.confidence_calculation.value] = cell_phrase
        return TableProduct(row_dict)

    def _save_to_file(self, table_items: list[TableProduct]):
        table_json = json.dumps(table_items, indent=4, cls=JsonEncoder, ensure_ascii=False)
        with open(ConfigConsts.DIRECTORY_TO_SAVE + self.__FINAL_TABLE_OUTPUT_PATH_PREFIX,
                  mode="w", encoding="utf-8") as f:
            f.write(table_json)
