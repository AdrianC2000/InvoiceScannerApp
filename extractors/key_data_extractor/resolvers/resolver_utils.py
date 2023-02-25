from entities.key_data_processing.block_position import BlockPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from invoice_processing_utils.common_utils import check_percentage_inclusion


def remove_redundant_lines(matching_block: MatchingBlock) -> MatchingBlock:
    """ Remove lines that are above the line in which key word is located -> key values cannot be there """
    key_word_index = matching_block.row_index
    matching_block.block.rows = matching_block.block.rows[key_word_index:]
    return matching_block


def has_numbers(word: str) -> bool:
    return any(char.isdigit() for char in word)


def get_closest_block_on_the_right(all_blocks: list[BlockPosition], key_row_position: Position, row_starting_y: int,
                                   row_ending_y: int) -> BlockPosition:
    threshold = 30
    extended_row_starting_y = row_starting_y - threshold
    extended_row_ending_y = row_ending_y + threshold
    try:
        block_on_the_right = _find_closest_block_on_the_right(all_blocks, key_row_position, extended_row_starting_y,
                                                              extended_row_ending_y)
    except IndexError:
        block_on_the_right = _find_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y,
                                                              row_ending_y)
    return block_on_the_right


def _find_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y) -> BlockPosition:
    closest_block_on_the_right, closest_distance = None, 10000
    for block in all_blocks:
        percentage = check_percentage_inclusion(row_starting_y, row_ending_y, block.position.starting_y,
                                                block.position.ending_y)
        if percentage != 0:
            row_ending_x = key_row_position.ending_x
            block_starting_x = block.position.starting_x
            if ((block_starting_x - row_ending_x) < closest_distance) and (row_ending_x < block_starting_x):
                closest_distance = block_starting_x - row_ending_x
                closest_block_on_the_right = block
    return closest_block_on_the_right


def get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    """ Finding the closest block below the block with the key word based on the position of the key words row """
    threshold = 300
    extended_row_starting_x = row_starting_x - threshold
    extended_row_ending_x = row_ending_x + threshold
    try:
        block_below = _get_closest_block_below(all_blocks, key_row_position,
                                               extended_row_starting_x, extended_row_ending_x)
    except IndexError:
        block_below = _get_closest_block_below(all_blocks, key_row_position,
                                               row_starting_x, row_ending_x)
    return block_below


def _get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    closest_block_below, closest_distance = None, 10000
    for block in all_blocks:
        percentage = check_percentage_inclusion(row_starting_x, row_ending_x, block.position.starting_x,
                                                block.position.ending_x)
        if percentage != 0:
            row_ending_y = key_row_position.ending_y
            block_starting_y = block.position.starting_y
            if ((block_starting_y - row_ending_y) < closest_distance) and (row_ending_y < block_starting_y):
                closest_block_below = block
                closest_distance = block_starting_y - row_ending_y
    return closest_block_below
