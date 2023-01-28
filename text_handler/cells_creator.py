import logging

from entities.table_processing.cell import Cell
from entities.table_processing.column import Column
from entities.common.position import Position
from entities.table_processing.row import Row
from entities.table_processing.table import Table
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import check_percentage_inclusion


def parse_data_into_table(cells_content: list[list[list[TextPosition]]]) -> Table:
    rows = list()
    for row in cells_content:
        cells_in_row = list()
        for cell in row:
            cell = Cell(cell)
            cells_in_row.append(cell)
        rows.append(Row(cells_in_row))
    return Table(rows)


class CellsCreator:
    """ Aligning words to columns in correct order """

    def __init__(self, texts_with_positions: list[TextPosition], cells_in_columns: list[Column]):
        self.__texts_with_positions = texts_with_positions
        self.__cells_in_columns = cells_in_columns

    def align_words_to_cells(self) -> Table:
        cells_content = self.generate_empty_table()

        for text_position in self.__texts_with_positions:
            coordinates = text_position.position
            column_index, confidence_column = self.check_column_belonging(coordinates)
            row_index, confidence_row = self.check_row_belonging(coordinates)
            cells_content[row_index][column_index].append(text_position)

        return parse_data_into_table(cells_content)

    def generate_empty_table(self):
        empty_cells = list()
        columns_number = len(self.__cells_in_columns)
        rows_number = len(self.__cells_in_columns[0].cells)
        for row in range(rows_number):
            cell = list()
            for column in range(columns_number):
                cell.append(list())
            empty_cells.append(cell)
        logging.info(f'Columns number: {columns_number}, Rows number: {rows_number}')
        return empty_cells

    def check_column_belonging(self, coordinates: Position) -> tuple[int, float]:
        """ Calculating which column is given cell in """
        for index, column in enumerate(self.__cells_in_columns):
            column_starting_x = column.cells[0].starting_x
            column_ending_x = column.cells[0].starting_x + column.cells[0].ending_x
            percentage = check_percentage_inclusion(coordinates.starting_x, coordinates.ending_x, column_starting_x,
                                                    column_ending_x)
            if percentage != 0:
                return index, percentage

    def check_row_belonging(self, coordinates: Position) -> tuple[int, float]:
        """ Calculating which row is given cell in """
        # TODO -> case, when a "word" floods over the row (for example api made a mistake and merge two signs from
        #  two separate cells into one -> extended parsing needed
        for index, cell in enumerate(self.__cells_in_columns[0].cells):
            row_starting_y = cell.starting_y
            row_ending_y = cell.starting_y + cell.ending_y
            percentage = check_percentage_inclusion(coordinates.starting_y, coordinates.ending_y, row_starting_y,
                                                    row_ending_y)
            if percentage != 0:
                return index, percentage
