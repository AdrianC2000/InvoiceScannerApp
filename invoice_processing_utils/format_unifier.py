import logging
import numpy

from pdf2image import convert_from_path
from werkzeug.datastructures import FileStorage
from numpy import ndarray
from PIL import Image
from settings.config_consts import ConfigConsts


class InvoiceFormatUnifier:
    def __init__(self, invoice_directory_path: str):
        self.__invoice_directory_path = invoice_directory_path

    def unify_format(self, invoice_file: FileStorage) -> ndarray:
        if invoice_file.filename.endswith("pdf"):
            with open(self.__invoice_directory_path, 'wb') as f:
                f.write(invoice_file.stream.read())
            pages = convert_from_path(self.__invoice_directory_path, poppler_path=ConfigConsts.POPPLER_PATH)
            image = pages[0]
        else:
            image = Image.open(invoice_file.stream)
        logging.info(f'File received -> size: {image.size}')
        return numpy.array(image.convert('RGB'))
