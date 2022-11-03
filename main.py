from skimage import io
from invoice_processor.invoice_straightener import InvoiceStraightener
from processors.data_processor import DataProcessor
from processors.table_processor import TableProcessor

if __name__ == "__main__":
    file_path = "resources/censored_invoices/Invoice 1 faked data.png"
    invoice_image = io.imread(file_path)[:, :, :3]

    straightened_invoice = InvoiceStraightener(invoice_image).straighten_image()

    parsed_rows, invoice_without_table = TableProcessor(straightened_invoice).extract_table_data()
    parsed_data = DataProcessor(invoice_without_table).extract_key_data()
