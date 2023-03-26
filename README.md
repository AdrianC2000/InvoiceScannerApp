# InvoiceScanner

## 1. Introduction
InvoiceScanner is a complex tool that automatically scans given invoice document and extracts crucial data from it. After extraction, user can modify the data (introduce corrections) or set some configurable parameters in the configuration panel in order to customize the output. What is more, application supports sending the data to the specified endpoint (e.g. to the application that serves as a tax settlement tool). Those features make InvoiceScanner a perfect tool for people who are fed up with a tedious job of rewriting invoices manually and placing the data into the system. <br>
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
2. <b> Key values </b>:
    * data for buyes and seller:
      * name
      * address
      * tax identification number (NIP)
    * listing date
    * invoice id
    * currency
### Application's user interface functionalities
There are three main panels:
1. <b> Main view panel, </b> where user can sumbit the invoices, and receive the extracted data. Here are the navigation buttons for the configuration panel and the data sending panel. 
2. <b> Configuration panel, </b> where user can specify three categories of settings:
   1. Endpoint configuration
   2. Request headers configuration 
   3. Data configuration - user can select which values should be omitted, what keys should be used and add some other options, like empty data removal.
3. <b> External API response panel, </b> where after sending the data to the given endpoint JSON that was received as a response is presented.

## 3. Invoice documents requirements
1. Presented version supports only invoices in polish language (but switching the app to handle new language is pretty straightforward and required changes that are described in the *file* file). 
2. Table product contains borders - bordeless tables are currently not supported.
3. Only supported file types are jpg, png and pdf - for pdf files each page is processed as separated invoice (multipage invoices are not supported). 
4. Invoice contains typical words and phrases which allow the invoice to be parsed.

## 4. Project structure
<img src="https://github.com/AdrianC2000/InvoiceScannerApp/blob/main/docs_images/application_structure.png"  width="50%" height="50%"> <br> <br>
### Backend
### API
### Frontend

## 5. Tests

## 6. Future work
Application is still under the development - more features and functionalities to come!
