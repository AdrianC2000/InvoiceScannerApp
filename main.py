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

# make a POST request
import json

import requests

from settings.settings import dump_to_json

dictToSend = {
        "invoice": {
            "services": [
                {
                    "name": "Sprzedaży energii elektrycznej",
                    "quantity": "77",
                    "net_price": "2221",
                    "tax_symbol": "23",
                    "gross_price": "2732"
                },
                {
                    "name": "Świadczonych usług dystrybucji",
                    "quantity": "77",
                    "net_price": "1426",
                    "tax_symbol": "23",
                    "gross_price": "1754"
                },
                {
                    "name": "Sprzedaży energii elektrycznej",
                    "quantity": "237",
                    "net_price": "11215",
                    "tax_symbol": "5",
                    "gross_price": "11776"
                },
                {
                    "name": "Świadczonych usług dystrybucji",
                    "quantity": "237",
                    "net_price": "8365",
                    "tax_symbol": "5",
                    "gross_price": "8783"
                }
            ],
            "client_company_name": "Adrian Ciesielczyk UI. Niewiadomo 10A 33-100 Tarnów NIP: 1122334455",
            "invoice_number": "E/TM/0308837/22",
            "currency": "PLN",
            "listing_date": "16/02/2022"
        }
    }
res = requests.post('https://api.infakt.pl/v3/invoices.json', json=dictToSend, headers={
    "Content-Type": "application/json",
    "X-inFakt-ApiKey": "49139f268c535563e40faf7f1eb52e0d9b8f8e0b"
})
print('response from server:', res.text)
dictFromServer = res.json()
print(res.text)
