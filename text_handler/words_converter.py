import warnings
import pandas as pd

from entities.table_processing.row_content import RowContent
from entities.table_processing.table import Table
from invoice_processing_utils.common_utils import check_percentage_inclusion, SIGNS_WITHOUT_SPACE_AFTER, \
    SIGNS_WITHOUT_SPACE_BEFORE
from settings.config_consts import ConfigConsts
from entities.common.text_position import TextPosition

warnings.simplefilter(action='ignore', category=FutureWarning)


class WordsConverter:
    __EXTRACTED_TABLE_OUTPUT_PATH_PREFIX = "8.Extracted table.xlsx"

    def __init__(self, table: Table):
        self.__table = table

    def merge_words_into_phrases(self) -> list[RowContent]:
        cells_with_phrases = list()
        for rows in self.__table.rows:
            row_cells = list()
            for cells in rows.cells:
                rows_in_cell = list()
                for text_position in cells.text_positions:
                    self._process_single_text_in_cell(rows_in_cell, text_position)
                final_phrase_in_cell = self._append_text_to_final_phrase(rows_in_cell)
                row_cells.append(final_phrase_in_cell)
            cells_with_phrases.append(RowContent(row_cells))
        self._write_to_xls(cells_with_phrases)
        return cells_with_phrases

    def _process_single_text_in_cell(self, rows_in_cell: list[TextPosition], text_position: TextPosition):
        if len(rows_in_cell) == 0:
            rows_in_cell.append(text_position)
        else:
            row_number, is_row_already_present = self._get_row_number(rows_in_cell, text_position)
            if is_row_already_present:
                actual_text = rows_in_cell[row_number].text
                new_text = self._get_new_text(actual_text, text_position.text)
                rows_in_cell[row_number].text = new_text
            else:
                rows_in_cell.insert(row_number, text_position)

    @staticmethod
    def _get_row_number(rows_in_cell: list[TextPosition], text_position: TextPosition) -> tuple[int, bool]:
        for index, row in enumerate(rows_in_cell):
            percentage = check_percentage_inclusion(text_position.position.starting_y, text_position.position.ending_y,
                                                    row.position.starting_y, row.position.ending_y)
            if percentage > 50:
                return index, True
        # At this point it is known that the word is not inside any of the existing cells
        starting_y = rows_in_cell[0].position.starting_y
        if text_position.position.ending_y <= starting_y:
            # Row does not exist yet, and is higher than any existing
            return -1, False
        for index, row in enumerate(rows_in_cell):
            # Looking for the first row that is below the word
            ending_y = row.position.ending_y
            if text_position.position.starting_y < ending_y:
                return index, False
        # Row does not exist yet, and is lower than any existing
        return len(rows_in_cell), False

    @staticmethod
    def _get_new_text(actual_text: str, text: str) -> str:
        if actual_text[-1] in SIGNS_WITHOUT_SPACE_AFTER or text[0] in SIGNS_WITHOUT_SPACE_BEFORE:
            return actual_text + text
        else:
            return actual_text + " " + text

    @staticmethod
    def _append_text_to_final_phrase(rows_in_cell: list[TextPosition]) -> str:
        final_phrase_in_cell = ""
        for row in rows_in_cell:
            if final_phrase_in_cell == "":
                final_phrase_in_cell = row.text
            else:
                final_phrase_in_cell = final_phrase_in_cell + " " + row.text
        return final_phrase_in_cell

    def _write_to_xls(self, rows_content: list[RowContent]):
        df = pd.DataFrame(list(row_content.cells_content for row_content in rows_content))
        writer = pd.ExcelWriter(ConfigConsts.DIRECTORY_TO_SAVE + self.__EXTRACTED_TABLE_OUTPUT_PATH_PREFIX,
                                engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}})
        df.to_excel(writer, sheet_name='Extracted table', index=False)
        writer.close()
