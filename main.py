# import json
#
# from skimage import io
# from parsers.json_encoder import JsonEncoder
# from processors.invoice_info_processor import InvoiceInfoProcessor
#
# if __name__ == "__main__":
#     file_path = "resources/censored_invoices/Invoice 1 faked data.png"
#     invoice_image = io.imread(file_path)[:, :, :3]
#
#     invoice_info = InvoiceInfoProcessor(invoice_image).extract_info()
#     print(json.dumps(invoice_info, indent=4, cls=JsonEncoder, ensure_ascii=False))