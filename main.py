from invoice_straightener.invoice_straightener import InvoiceStraightener
from table_extractor.table_extractor import TableExtractor
import cv2


if __name__ == "__main__":
    file_path = "resources/censored_invoices/Invoice 1 censored.png"
    output_straightened_path = "resources/straightened_invoices/Invoice 1 straightened.png"
    output_extracted_table = "resources/extracted_tabled/Invoice 1 extracted table.png"

    straightened_invoice = InvoiceStraightener(file_path).straighten_image()
    cv2.imwrite(output_straightened_path, straightened_invoice)

    table = TableExtractor(output_straightened_path).extract_table()
    print(f"Writing image to {output_extracted_table}")
    cv2.imwrite(output_extracted_table, table)
