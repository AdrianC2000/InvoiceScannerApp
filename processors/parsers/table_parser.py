import json

from classifiers.headers_classifier.model.matching_headers import MatchingHeaders
from processors.model.parsed_table import ParsedTable
from entities.table_processing.row_content import RowContent
from invoice_processing_utils.json_encoder import JsonEncoder
from processors.model.table_product import TableProduct
from settings.config_consts import ConfigConsts


class TableParser:

    __FINAL_TABLE_OUTPUT_PATH_PREFIX = "9.Final table.json"

    def get_table_content(self, matching_headers: MatchingHeaders, rows_content: list[RowContent]) -> ParsedTable:
        table_items = list()
        for row in rows_content:
            table_product = self._parse_row_to_table_product(row, matching_headers)
            table_items.append(table_product)
        product_rows = table_items[1:len(table_items)]
        self._save_to_file(product_rows)
        return ParsedTable(product_rows)

    @staticmethod
    def _parse_row_to_table_product(row: RowContent, matching_headers: MatchingHeaders) -> TableProduct:
        row_dict = dict()
        for index, cell_phrase in enumerate(row.cells_content):
            matching_header = matching_headers.get_by_column_index(index)
            if matching_header:
                row_dict[matching_header.confidence_calculation.value] = cell_phrase
        return TableProduct(row_dict)

    def _save_to_file(self, table_items: list[TableProduct]):
        table_json = json.dumps(table_items, indent=4, cls=JsonEncoder, ensure_ascii=False)
        with open(ConfigConsts.DIRECTORY_TO_SAVE + self.__FINAL_TABLE_OUTPUT_PATH_PREFIX,
                  mode="w", encoding="utf-8") as f:
            f.write(table_json)
