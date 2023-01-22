import logging

import numpy
from pdf2image import convert_from_path
from werkzeug.datastructures import FileStorage

from numpy import ndarray
from PIL import Image


class FormatUnifier:
    __POPPLER_PATH = r"C:\Users\adria\poppler-0.68.0\bin"

    def __init__(self, path: str, invoice_file: FileStorage):
        self.__path = path
        self.__invoice_file = invoice_file

    def unify_format(self) -> ndarray:
        filename = self.__invoice_file.filename
        if filename.endswith("pdf"):
            with open(self.__path + "/" + filename, 'wb') as f:
                f.write(self.__invoice_file.stream.read())
            pages = convert_from_path(self.__path + "/" + filename, poppler_path=self.__POPPLER_PATH)
            image = pages[0]
        else:
            image = Image.open(self.__invoice_file.stream)
        logging.info(f'File received -> size {image.size}')
        return numpy.array(image.convert('RGB'))
