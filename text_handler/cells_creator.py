class CellsCreator:

    def __init__(self, text_with_position, cells_in_columns):
        self.text_with_position = text_with_position
        self.cells_in_columns = cells_in_columns

    def align_words_to_cells(self):
        for word_text, coordinates in self.text_with_position.items():
            column_index, confidence = self.check_column_belonging(coordinates)
            print(f"{word_text} belongs to the column: {column_index} with a confidence of {confidence}%")

    def check_column_belonging(self, coordinates):
        index = 1
        # TODO -> handle first 'column'
        cells_in_columns = self.cells_in_columns[1:]
        for column in cells_in_columns:
            column_starting_x = column[0][0]
            column_ending_x = column[0][0] + column[0][2]
            if (column_starting_x <= coordinates[0]) and (column_ending_x >= coordinates[2]):
                return index, 100
            elif coordinates[0] < column_starting_x < coordinates[2]:
                common_start = column_starting_x
                common_end = coordinates[2]
                common_length = common_end - common_start
                word_length = coordinates[2] - coordinates[0]
                percentage = common_length / word_length * 100
                if percentage > 50:
                    return index, percentage
            elif coordinates[0] < column_ending_x < coordinates[2]:
                common_start = coordinates[0]
                common_end = column_ending_x
                common_length = common_end - common_start
                word_length = coordinates[2] - coordinates[0]
                percentage = common_length / word_length * 100
                if percentage > 50:
                    return index, percentage
            index += 1
