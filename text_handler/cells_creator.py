import logging
from typing import List, Tuple

from text_handler.model.cell import Cell
from columns_separator.model.column import Column
from entities.common.position import Position
from text_handler.model.row import Row
from text_handler.model.table import Table
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import check_percentage_inclusion


class CellsCreator:
    """ Aligning words to columns in correct order """

    def align_words_to_cells(self, texts_with_positions: List[TextPosition], cells_in_columns: List[Column]) -> Table:
        cells_content = self._generate_empty_table(cells_in_columns)

        for text_position in texts_with_positions:
            coordinates = text_position.position
            column_index, confidence_column = self._check_column_belonging(coordinates, cells_in_columns)
            row_index, confidence_row = self._check_row_belonging(coordinates, cells_in_columns[0])
            cells_content[row_index][column_index].append(text_position)

        return self._parse_data_into_table(cells_content)

    @staticmethod
    def _generate_empty_table(cells_in_columns: List[Column]) -> List[List[List]]:
        empty_cells = []
        columns_number = len(cells_in_columns)
        rows_number = len(cells_in_columns[0].cells)
        for _ in range(rows_number):
            cell = []
            for _ in range(columns_number):
                cell.append([])
            empty_cells.append(cell)
        logging.info(f'Columns number: {columns_number}, Rows number: {rows_number}')
        return empty_cells

    @staticmethod
    def _check_column_belonging(coordinates: Position, cells_in_columns: List[Column]) -> Tuple[int, float]:
        """ Calculating which column is given cell in """

        for index, column in enumerate(cells_in_columns):
            column_starting_x = column.cells[0].starting_x
            column_ending_x = column.cells[0].starting_x + column.cells[0].ending_x
            percentage = check_percentage_inclusion(coordinates.starting_x, coordinates.ending_x, column_starting_x,
                                                    column_ending_x)
            if percentage != 0:
                return index, percentage

    @staticmethod
    def _check_row_belonging(coordinates: Position, first_column: Column) -> Tuple[int, float]:
        """ Calculating which row is given cell in """

        for index, cell in enumerate(first_column.cells):
            row_starting_y = cell.starting_y
            row_ending_y = cell.starting_y + cell.ending_y
            percentage = check_percentage_inclusion(coordinates.starting_y, coordinates.ending_y, row_starting_y,
                                                    row_ending_y)
            if percentage != 0:
                return index, percentage

    @staticmethod
    def _parse_data_into_table(cells_content: List[List[List[TextPosition]]]) -> Table:
        rows = []
        for row in cells_content:
            cells_in_row = []
            for cell in row:
                cell = Cell(cell)
                cells_in_row.append(cell)
            rows.append(Row(cells_in_row))
        return Table(rows)
