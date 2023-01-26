import logging

from entities.column import Column
from entities.position import Position
from entities.text_position import TextPosition


def check_percentage_inclusion(inner_object_starting: int, inner_object_ending: int, outer_object_starting: int,
                               outer_object_ending: int) -> float:
    if (outer_object_starting <= inner_object_starting) and (outer_object_ending >= inner_object_ending):
        return 100
    elif inner_object_starting < outer_object_starting < inner_object_ending:
        common_start = inner_object_starting
        common_end = inner_object_ending
        common_length = common_end - common_start
        word_length = inner_object_ending - inner_object_starting
        percentage = common_length / word_length * 100
        if percentage > 50:
            return percentage
    elif inner_object_starting < outer_object_ending < inner_object_ending:
        common_start = inner_object_starting
        common_end = outer_object_ending
        common_length = common_end - common_start
        word_length = inner_object_ending - inner_object_starting
        percentage = common_length / word_length * 100
        if percentage > 50:
            return percentage
    return 0


class CellsCreator:

    def __init__(self, texts_with_positions: list[TextPosition], cells_in_columns: list[Column]):
        self.__texts_with_positions = texts_with_positions
        self.__cells_in_columns = cells_in_columns

    def align_words_to_cells(self) -> list[list[list[TextPosition]]]:
        # TODO -> implement entities for that nested lists - list of words in the cell -> list of cells -> list of rows
        # Aligning words to columns
        cells_content = []
        columns_number = len(self.__cells_in_columns) - 1
        rows_number = len(self.__cells_in_columns[1].cells)
        for columns in range(rows_number):
            cell = []
            for row in range(columns_number):
                cell.append([])
            cells_content.append(cell)

        for text_position in self.__texts_with_positions:
            coordinates = text_position.position
            column_index, confidence_column = self.check_column_belonging(coordinates)
            row_index, confidence_row = self.check_row_belonging(coordinates)

            cells_content[row_index][column_index].append(text_position)

        logging.info(f'Columns number: {columns_number}, Rows number: {rows_number}')
        return cells_content

    def check_column_belonging(self, coordinates: Position) -> tuple[int, float]:
        index = 0
        cells_in_columns = self.__cells_in_columns[1:]
        for column in cells_in_columns:
            column_starting_x = column.cells[0].starting_x
            column_ending_x = column.cells[0].starting_x + column.cells[0].ending_x
            percentage = check_percentage_inclusion(coordinates.starting_x, coordinates.ending_x, column_starting_x,
                                                    column_ending_x)
            if percentage != 0:
                return index, percentage
            index += 1

    def check_row_belonging(self, coordinates: Position) -> tuple[int, float]:
        index = 0
        # TODO -> case, when a "word" floods over the row (for example api made a mistake and merge two signs from
        #  two separate cells into one -> extended parsing needed
        cells_in_columns = self.__cells_in_columns[1:]
        for cell in cells_in_columns[0].cells:
            row_starting_y = cell.starting_y
            row_ending_y = cell.starting_y + cell.ending_y
            percentage = check_percentage_inclusion(coordinates.starting_y, coordinates.ending_y, row_starting_y,
                                                    row_ending_y)
            if percentage != 0:
                return index, percentage
            index += 1
