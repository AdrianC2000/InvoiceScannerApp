import warnings
import pandas as pd

from entities.table_processing.row_content import RowContent
from entities.table_processing.table import Table
from text_handler.cells_creator import check_percentage_inclusion
from settings.config_consts import ConfigConsts
from entities.common.text_position import TextPosition

warnings.simplefilter(action='ignore', category=FutureWarning)

SIGNS_WITHOUT_SPACE_BEFORE = [')', ']', '}', ':', ',', ';', '.']
SIGNS_WITHOUT_SPACE_AFTER = ['(', '[', '{']
__EXTRACTED_TABLE_OUTPUT_PATH_PREFIX = "8.Extracted table.xlsx"


def get_row_number(rows_in_cell: list[TextPosition], text_position: TextPosition) -> int:
    index = 0
    for row in rows_in_cell:
        percentage = check_percentage_inclusion(text_position.position.starting_y, text_position.position.ending_y,
                                                row.position.starting_y, row.position.ending_y)
        if percentage > 50:
            return index
        index += 1
    starting_y = rows_in_cell[0].position.starting_y
    ending_y = rows_in_cell[-1].position.ending_y
    if text_position.position.ending_y <= starting_y:
        # Row does not exist yet, and is higher than any existing
        return -1
    if text_position.position.starting_y >= ending_y:
        # Row does not exist yet, and is lower than any existing
        return len(rows_in_cell)
    else:
        return -1


def append_text_to_final_phrase(rows_in_cell: list[TextPosition]) -> str:
    final_phrase_in_cell = ""
    for row in rows_in_cell:
        if final_phrase_in_cell == "":
            final_phrase_in_cell = row.text
        else:
            final_phrase_in_cell = final_phrase_in_cell + " " + row.text
    return final_phrase_in_cell


def write_to_xls(rows_content: list[RowContent]):
    df = pd.DataFrame([row_content.cells_content for row_content in rows_content])
    writer = pd.ExcelWriter(ConfigConsts.DIRECTORY_TO_SAVE + __EXTRACTED_TABLE_OUTPUT_PATH_PREFIX, engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_numbers': True}})
    df.to_excel(writer, sheet_name='Extracted table', index=False)
    writer.save()


def get_new_text(actual_text: str, text: str) -> str:
    if actual_text[-1] in SIGNS_WITHOUT_SPACE_AFTER or text[0] in SIGNS_WITHOUT_SPACE_BEFORE:
        return actual_text + text
    else:
        return actual_text + " " + text


def process_single_text_in_cell(rows_in_cell: list[TextPosition], text_position: TextPosition):
    if len(rows_in_cell) == 0:
        rows_in_cell.append(text_position)
    else:
        row_number = get_row_number(rows_in_cell, text_position)
        if row_number == -1:
            rows_in_cell.insert(0, text_position)
        elif row_number == len(rows_in_cell):
            rows_in_cell.append(text_position)
        else:
            actual_text = rows_in_cell[row_number].text
            new_text = get_new_text(actual_text, text_position.text)
            rows_in_cell[row_number].text = new_text


class WordsConverter:

    def __init__(self, table: Table):
        self.__table = table

    def merge_words_into_phrases(self) -> list[RowContent]:
        cells_with_phrases = list()
        for rows in self.__table.rows:
            row_cells = list()
            for cells in rows.cells:
                rows_in_cell = list()
                for text_position in cells.text_positions:
                    process_single_text_in_cell(rows_in_cell, text_position)
                final_phrase_in_cell = append_text_to_final_phrase(rows_in_cell)
                row_cells.append(final_phrase_in_cell)
            cells_with_phrases.append(RowContent(row_cells))
        write_to_xls(cells_with_phrases)
        return cells_with_phrases
