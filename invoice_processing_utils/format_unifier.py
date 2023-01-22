import logging
import numpy

from pdf2image import convert_from_path
from werkzeug.datastructures import FileStorage
from numpy import ndarray
from PIL import Image
from config import Config


class FormatUnifier:
    def __init__(self, path: str, invoice_file: FileStorage):
        self.__path = path
        self.__invoice_file = invoice_file

    def unify_format(self) -> ndarray:
        # TODO - handling every page
        filename = self.__invoice_file.filename
        if filename.endswith("pdf"):
            invoice_temp_file_path = f"{self.__path}/{filename}"
            with open(invoice_temp_file_path, 'wb') as f:
                f.write(self.__invoice_file.stream.read())
            pages = convert_from_path(invoice_temp_file_path, poppler_path=Config.POPPLER_PATH)
            image = pages[0]
        else:
            image = Image.open(self.__invoice_file.stream)
        logging.info(f'File received -> size: {image.size}')
        return numpy.array(image.convert('RGB'))
