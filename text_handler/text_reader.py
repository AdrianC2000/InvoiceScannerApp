import io
from collections import OrderedDict

from google.cloud import vision


class TextReader:

    def __init__(self, table_image_path):
        self.table_image_path = table_image_path

    def read_words(self):
        client = vision.ImageAnnotatorClient()

        with io.open(self.table_image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image, image_context={"language_hints": ["pl"]})
        text_with_position = {}

        for text in response.text_annotations[1::]:
            text_value = text.description
            start_x = text.bounding_poly.vertices[0].x
            start_y = text.bounding_poly.vertices[0].y
            end_x = text.bounding_poly.vertices[1].x
            end_y = text.bounding_poly.vertices[2].y
            print(f"StartX : {start_x}, StartY: {start_y}, EndX: {end_x}, EndY: {end_y}, text: {text_value}")
            text_with_position[text_value] = (start_x, start_y, end_x, end_y)

        return OrderedDict(sorted(text_with_position.items(), key=lambda s: s[1][2]))
