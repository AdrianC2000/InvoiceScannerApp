from skimage import io
import json
import os
import unittest

import numpy

from parsers.json_encoder import JsonEncoder
from processors.invoice_info_processor import InvoiceInfoProcessor
from settings import settings
from settings.settings import dump_to_json

import warnings


class InvoicesParsingTests(unittest.TestCase):
    __previous_configuration = None

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=FutureWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)

        cls.__previous_configuration = settings.get_configuration()
        with open('settings/configuration.json', mode="r", encoding="utf-8") as f:
            test_config = json.load(f)
        settings.set_configuration(json.dumps(test_config))

    def test_every_invoice(self):
        invoices_set = "tests/invoices_testing_set/"
        outputs_set = "tests/invoices_output_set/"
        cwd = os.getcwd()

        for file in os.listdir(os.fsencode(invoices_set)):
            filename = os.fsdecode(file)
            test_output_dir = cwd + '/tests/outputs/' + filename + "/"
            invoice_path = invoices_set + filename
            invoice_image = io.imread(invoice_path)[:, :, :3]
            invoice_info = InvoiceInfoProcessor(numpy.array(invoice_image), test_output_dir).extract_info()

            output_file = outputs_set + filename.split('.')[0] + ".json"
            f = open(output_file, mode="r", encoding="utf-8")
            output_json = json.load(f)

            expected_output = json.dumps(output_json, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)
            actual_output = json.dumps(invoice_info, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)

            with self.subTest(expected_output=expected_output):
                self.assertEqual(expected_output, actual_output, "Invoice info incorrect")

    # def test_single_invoice(self):
    #     invoices_set = "tests/invoices_testing_set/"
    #     outputs_set = "tests/invoices_output_set/"
    #     cwd = os.getcwd()
    #
    #     filename = "test_invoice_2.png"
    #     test_output_dir = cwd + '/tests/outputs/' + filename + "/"
    #
    #     if not os.path.exists(test_output_dir):
    #         os.makedirs(test_output_dir)
    #
    #     invoice_path = invoices_set + filename
    #     invoice_image = io.imread(invoice_path)[:, :, :3]
    #     invoice_info = InvoiceInfoProcessor(numpy.array(invoice_image), test_output_dir).extract_info()
    #
    #     output_file = outputs_set + filename.split('.')[0] + ".json"
    #     f = open(output_file, mode="r", encoding="utf-8")
    #     output_json = json.load(f)
    #
    #     expected_output = json.dumps(output_json, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)
    #     actual_output = json.dumps(invoice_info, indent=4, cls=JsonEncoder, ensure_ascii=False, sort_keys=True)
    #
    #     self.assertEqual(expected_output, actual_output, "Invoice info incorrect")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__previous_configuration))


if __name__ == '__main__':
    unittest.main()
