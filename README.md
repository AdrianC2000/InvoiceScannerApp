# InvoiceScanner

## Introduction
InvoiceScanner is a tool that automatically scans given invoice document and extracts crucial data from it. After extraction, user can modify the data (introduce corrections) or set some configurable parameters in the configuration panel in order to customize the output. What is more, application supports sending the data to the specified endpoint (e.g. to the application that serves as a tax settlement tool). Those features make InvoiceScanner a perfect tool for people who are fed up with a tedious job of rewriting invoices manually and placing the data into the system. <br>
Application implementation was the subject of an engineering thesis defended in January 2023 at the AGH University of Science and Technology in Kraków.

## Functionalities
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
1. <b> Main view panel </b>, where user can sumbit the invoices, and receive the extracted data. Here are the navigation buttons for the configuration panel and the data sending panel. 
2. <b> Configuration panel </b>, where user can specify three categories of settings:
  2.1 Endpoint configuration
  2.2 Request headers configuration 
  2.3 Data configuration - user can select which values should be omitted, what keys should be used and add some other options, like empty data removal.
3. <b> External API response panel </b> - after sending the data to the given endpoint panel presents the JSON that was received as a response. 

## Invoice documents requirements

## Project structure

## Tests

## Future work
Application is still under the development - more features and functionalities to come!
