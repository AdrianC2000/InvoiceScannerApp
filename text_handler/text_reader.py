from numpy import ndarray
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import get_ocr_response, create_position, save_image_with_bounding_boxes


class TextReader:

    __EXTRACTED_TEXTS_OUTPUT_PATH_PREFIX = "7.Extracted texts.png"

    def read_words(self, invoice_image: ndarray) -> list[TextPosition]:
        response = get_ocr_response(invoice_image)
        texts_with_positions = []

        for text in response.text_annotations[1::]:
            text_value = text.description
            texts_with_positions.append(TextPosition(text_value, create_position(text.bounding_poly)))

        save_image_with_bounding_boxes(invoice_image, self.__EXTRACTED_TEXTS_OUTPUT_PATH_PREFIX,
                                       [text_position.position for text_position in texts_with_positions])
        texts_with_positions.sort()
        return texts_with_positions
