import json
import os
import unittest
import numpy
import warnings
import numpy as np

from PIL import Image
from pdf2image import convert_from_path
from parsers.json_encoder import JsonEncoder
from processors.invoice_info_processor import InvoiceInfoProcessor


class InvoicesParsingTests(unittest.TestCase):
    __POPPLER_PATH = r"C:\Users\adria\poppler-0.68.0\bin"
    __tests_directory_path = "tests/invoice_parsing_end_to_end_tests"
    __invoices_set = __tests_directory_path + "/app_testing_set/"

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=FutureWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)
        cls.maxDiff = None

    # @unittest.skip('Comment this line to run the following test')
    def test_every_invoice(self):
        for file in os.listdir(os.fsencode(self.__invoices_set)):
            filename = os.fsdecode(file)
            print(f"Testing invoice {filename}")
            actual_output, expected_output = self.get_expected_and_actual_outputs(filename)

            with self.subTest(expected_output=expected_output, msg=filename):
                self.assertEqual(expected_output, actual_output, f"Invoice {filename} incorrect!")

    @unittest.skip('Comment this line to run the following test')
    def test_single_invoice(self):
        filename = "test_invoice_16.png"
        actual_output, expected_output = self.get_expected_and_actual_outputs(filename)

        self.assertEqual(expected_output, actual_output, f"Invoice {filename} incorrect!")

    def get_expected_and_actual_outputs(self, filename):
        test_output_dir = f"{os.getcwd()}/{self.__tests_directory_path}/outputs/{filename}/"

        if not os.path.exists(test_output_dir):
            os.makedirs(test_output_dir)

        invoice_path = f"{self.__tests_directory_path}/app_testing_set/{filename}"
        invoice_image = self.get_invoice_with_unified_format(filename, invoice_path)
        invoice_info = InvoiceInfoProcessor(numpy.array(invoice_image), test_output_dir).extract_info().invoice_info
        output_file = f"{self.__tests_directory_path}/invoices_output_set/{filename.split('.')[0]}.json"

        with open(output_file, encoding="utf-8") as fh:
            output_json = json.load(fh)

        expected_output = json.dumps(output_json, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)
        actual_output = json.dumps(invoice_info, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)
        return actual_output, expected_output

    def get_invoice_with_unified_format(self, filename, invoice_path):
        if filename.endswith("pdf"):
            pages = convert_from_path(invoice_path, poppler_path=self.__POPPLER_PATH)
            invoice_image = pages[0]  # TODO - add all pages handling
        else:
            invoice_image = np.array(Image.open(invoice_path))
        return invoice_image


if __name__ == '__main__':
    unittest.main()