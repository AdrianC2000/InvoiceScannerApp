import io
import cv2
from google.cloud import vision
from text_handler.entities.position import Position
from text_handler.entities.text_position import TextPosition


def save_table_with_bounding_boxes(table_image_path: str, texts_with_positions: list[TextPosition]):
    image = cv2.imread(table_image_path, 1)
    table_image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)
    for text_position in texts_with_positions:
        cv2.rectangle(table_image_copy, (text_position.position.starting_x, text_position.position.starting_y),
                      (text_position.position.ending_x, text_position.position.ending_y), 1)
    cv2.imwrite("resources/entire_flow/8.Extracted texts.png", table_image_copy)


class TextReader:

    def __init__(self, table_image_path: str):
        self.__table_image_path = table_image_path

    def read_words(self) -> list[TextPosition]:
        client = vision.ImageAnnotatorClient()

        with io.open(self.__table_image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image, image_context={"language_hints": ["pl"]})
        texts_with_positions = []

        for text in response.text_annotations[1::]:
            text_value = text.description
            start_x = text.bounding_poly.vertices[0].x
            start_y = text.bounding_poly.vertices[0].y
            end_x = text.bounding_poly.vertices[1].x
            end_y = text.bounding_poly.vertices[2].y
            texts_with_positions.append(TextPosition(text_value, Position(start_x, start_y, end_x, end_y)))

        save_table_with_bounding_boxes(self.__table_image_path, texts_with_positions)
        texts_with_positions.sort()
        return texts_with_positions
