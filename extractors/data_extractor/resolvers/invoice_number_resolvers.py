from classifiers.block_classifier.block_classifier import find_best_data_fit
from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.constants_key_words import number


def has_numbers(word: str) -> bool:
    return any(char.isdigit() for char in word)


class InvoiceNumberResolvers:

    def __init__(self, matching_block: MatchingBlock):
        self.__matching_block = matching_block

    def get_invoice_number(self) -> str:
        rows = self.__matching_block.block.rows
        row_with_invoice_number_key_text = rows[0].text
        _, number_index, confidence_calculation = find_best_data_fit(row_with_invoice_number_key_text, number)
        try:
            alleged_invoice_number = row_with_invoice_number_key_text.split(' ')[number_index + 1]
            if has_numbers(alleged_invoice_number):
                return alleged_invoice_number
            else:
                return ""  # TODO - searching down and right
        except IndexError:
            return ""  # TODO - searching down and right
