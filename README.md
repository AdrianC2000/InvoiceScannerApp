# InvoiceScanner

## 1. Introduction
InvoiceScanner is a complex tool that automatically scans given invoice document and extracts crucial data from it. After extraction, user can modify the data (introduce corrections) or set some configurable parameters in the configuration panel in order to customize the output. Moreover, the application supports sending the data to the specified endpoint (e.g. to the application that serves as a tax settlement tool). Those features make InvoiceScanner a perfect tool for people who are fed up with the tedious job of rewriting invoices manually and placing the data into the system. <br>
Application implementation was the subject of an engineering thesis defended in January 2023 at the AGH University of Science and Technology in Kraków.

## 2. Functionalities
### Extracted data
Data that is extracted by the application includes two main categories:
1. <b> Products table data </b> - for each position following data is searched:
    * ordinal number
    * name
    * pkwiu
    * quantity
    * unit of measure
    * gross price
    * gross value
    * net price
    * net value
    * vat
    * vat value
![main panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/table_data_extraction.gif) <be>
More information about the table extraction process can be found on the [```extractors``` module](https://github.com/AdrianC2000/InvoiceScannerApp/wiki/Extractors-module), [```column separator``` module](https://github.com/AdrianC2000/InvoiceScannerApp/wiki/Column-seperator-module), and [```classifiers``` module](https://github.com/AdrianC2000/InvoiceScannerApp/wiki/Classifiers-module) wiki pages. 

2. <b> Key values </b>:
    * data for buyer and seller:
      * name
      * address
      * tax identification number (NIP)
    * listing date
    * invoice id
    * currency
![main panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/key_data_extraction.gif) <be>
More information about the key data extraction process can be found on the [```extractors``` module](https://github.com/AdrianC2000/InvoiceScannerApp/wiki/Extractors-module) and [```classifiers``` module](https://github.com/AdrianC2000/InvoiceScannerApp/wiki/Classifiers-module) wiki pages. 

### Sample input invoice presented on the gifs:
![main panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/test_invoice.png)

### Sample output:
```json
{
    "buyer_address": "al. Kijowska 50 33-120 Kraków",
    "buyer_name": "Adrian Ciesielczyk",
    "buyer_nip": "1112223334",
    "currency": "PLN",
    "invoice_number": "01/11/2022",
    "listing_date": "07-11-2022",
    "table_products": [
        {
            "gross_price": null,
            "gross_value": "290,40",
            "name": "Produkt 123",
            "net_price": "120,00",
            "net_value": "240,00",
            "ordinal_number": "1",
            "pkwiu": null,
            "quantity": "2",
            "unit_of_measure": "szt.",
            "vat": "23 %",
            "vat_value": "50,40"
        },
        {
            "gross_price": null,
            "gross_value": "300,00",
            "name": "Produkt produkt 345",
            "net_price": "50,00",
            "net_value": "250,00",
            "ordinal_number": "2",
            "pkwiu": null,
            "quantity": "5",
            "unit_of_measure": "szt.",
            "vat": "23 %",
            "vat_value": "50,00"
        },
        {
            "gross_price": null,
            "gross_value": "762,00",
            "name": "Abc abc 123",
            "net_price": "60,00",
            "net_value": "600,00",
            "ordinal_number": "3",
            "pkwiu": null,
            "quantity": "10",
            "unit_of_measure": "szt.",
            "vat": "23 %",
            "vat_value": "162,00"
        }
    ],
    "seller_address": "ul. Czarnowiejska 50 33-312 Kraków",
    "seller_name": "Firma 123",
    "seller_nip": "1112223334"
}
```

### Application's user interface functionalities
There are three main panels:
1. <b> Main view panel, </b> where user can submit the invoices, and receive the extracted data. Here are the navigation buttons for the configuration panel and the data sending panel.
![main panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/main_panel.png) <br>
3. <b> Configuration panel, </b> where user can specify three categories of settings:
   1. Endpoint configuration
   2. Request headers configuration 
   3. Data configuration - user can select which values should be omitted, what keys should be used and add some other options, like empty data removal.
![settings panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/settings_panel.png) <br>
4. <b> External API response panel, </b> where after sending the data to the given endpoint JSON that was received as a response is presented.
![response panel](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/response_panel.png)

## 3. Invoice documents requirements
1. The presented version supports only invoices in the Polish language (but switching the app to handle a new language is pretty straightforward and only requires changes in the headers and key data labels - check [table_headers_database.json](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/classifiers/headers_classifier/table_headers_database.json) and [key_words_database.json](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/classifiers/block_classifier/key_words_database.json)). 
2. Table product contains borders - borderless tables are currently not supported. (this feature is on the roadmap :)
3. Only supported file types are jpg, png and pdf - for pdf files each page is processed as separated invoice (multi page invoices are not supported yet). 
4. Invoice contains typical words and phrases that allow the invoice to be parsed.

## 4. Project structure
<img src="https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/application_structure.png"  width="50%" height="50%"> <br> <br>
### Backend
Implemented with Python 3.12 and libraries such as:
* open-cv
* numpy
* pillow
* Levenshtein
* Google Cloud Vision OCR

### API
Implemented with Flask, serves as a communication point between the backend and UI. 

### Frontend
Implemented with electron.js and react frameworks, so that the application can run as a desktop app. 

## 5. Tests
Tests are available [here](https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/tests/) - put some of your invoices in the ```tests/invoice_parsing_end_to_end_tests/app_testing_set/``` and run tests from the ```invoices_parsing_tests.py``` file. 
Tests output will be available in the ```tests/invoice_parsing_end_to_end_tests/outputs/invoice_output_set``` and ```tests/invoice_parsing_end_to_end_tests/outputs```

For more information about the project and its implementation check [projects wiki](https://github.com/AdrianC2000/InvoiceScannerApp/wiki)

## 6. Future work
Most important features that are researched:
* Borderless products table processing 
* New languages handling
* Multi page invoices support
* Additional panel letting user fast verification of the extracted data

The application is still under development - more features and functionalities to come!
