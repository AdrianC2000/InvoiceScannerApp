import json

from classifiers.entities.matching_block import MatchingBlock
from classifiers.headers_classifier.headers_classifier import find_best_data_fit
from text_handler.entities.block_position import BlockPosition


def load_data():
    f = open('data_extractor/temporary_data_database.json', mode="r", encoding="utf-8")
    return json.load(f)


def remove_duplicates(filtered_matching_blocks: list[MatchingBlock]) -> list[MatchingBlock]:
    removed_duplicated_list = list()
    for matching_block in filtered_matching_blocks:
        actual_key = matching_block.confidence_calculation.value
        actual_confidence = matching_block.confidence_calculation.confidence
        if any(block.confidence_calculation.value == actual_key for block in removed_duplicated_list):
            block_with_the_same_key = [block for block in removed_duplicated_list
                                       if block.confidence_calculation.value == actual_key][0]
            if block_with_the_same_key.confidence_calculation.confidence < actual_confidence:
                removed_duplicated_list.remove(block_with_the_same_key)
                removed_duplicated_list.append(matching_block)
        else:
            removed_duplicated_list.append(matching_block)
    return removed_duplicated_list


class DataExtractor:

    def __init__(self, block_positions: list[BlockPosition]):
        self.block_positions = block_positions

    def extract_data(self) -> list[MatchingBlock]:
        percentage_calculation, index = "", 0
        data_patterns = load_data()
        matching_blocks = list()
        for block in self.block_positions:
            for index, row in enumerate(block.rows):
                percentage_calculation = find_best_data_fit(row.text, data_patterns)
                if percentage_calculation.confidence > 0.9:
                    del data_patterns[percentage_calculation.value]
                    break
            matching_blocks.append(MatchingBlock(block, percentage_calculation, index))
        filtered_matching_blocks = [block for block in matching_blocks if block.confidence_calculation.confidence > 0.5]
        unique_keys_blocks = remove_duplicates(filtered_matching_blocks)
        return unique_keys_blocks
