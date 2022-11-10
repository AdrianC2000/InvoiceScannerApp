SETTINGS = {
    "url_configuration": {
        "url": "https://api.infakt.pl/v3/invoices.json",
        "separately": "true"
    },
    "headers_configuration": {
         "Content-Type": "application/json",
         "X-inFakt-ApiKey": "49139f268c535563e40faf7f1eb52e0d9b8f8e0b"
    },
    "data_configuration": {
         "remove_nulls": "true",
         "ordinal_number": {
             "value": "ordinal_number",
             "included": "true"
         },
         "name": {
             "value": "name",
             "included": "true"
         }, 
         "pkwiu": {
             "value": "pkwiu",
             "included": "false"
         },
         "quantity": {
             "value": "quantity123",
             "included": "true"
         },
         "unit_of_measure": {
             "value": "unit_of_measureeeeeee",
             "included": "true"
         },
         "gross_price": {
             "value": "gross_price",
             "included": "true"
         }, 
         "net_price": {
             "value": "net_price",
             "included": "true"
         },
         "net_value": {
             "value": "net_value",
             "included": "true"
         },
         "vat": {
             "value": "vat",
             "included": "true"
         },
         "vat_value": {
             "value": "vat_value",
             "included": "true"
         },
         "gross_value": {
             "value": "gross_value",
             "included": "true"
         }, 
         "seller": {
             "value": "seller",
             "included": "true"
         },
         "buyer": {
             "value": "buyer",
             "included": "true"
         },
         "invoice_number": {
             "value": "invoice_number",
             "included": "true"
         },
         "currency": {
             "value": "currency",
             "included": "true"
         },
         "listing_date": {
             "value": "listing_date",
             "included": "true"
         }
    }
}