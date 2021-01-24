from PyPDF2 import PdfFileReader
from process1.invoice_parsers import (
    RoboProInvoiceParser,
    GymInvoiceParser,
    SaasInvoiceParser
)


class InvoiceReader:

    @classmethod
    def read_pdf(cls, filename: str):
        with open(filename, 'rb') as invoice_file:
            pdf = PdfFileReader(invoice_file)
            invoice = pdf.getPage(0)
            lines = [line.strip() for line in invoice.extractText().split('\n') if line.strip()]
            return lines

    @staticmethod
    def __pick_parser(filename: str):
        filename = filename.lower()
        if "gym" in filename:
            return GymInvoiceParser
        elif "saas" in filename:
            return SaasInvoiceParser
        else:
            return RoboProInvoiceParser

    @classmethod
    def parse_invoice(cls, filename: str):
        parser = cls.__pick_parser(filename)
        lines = cls.read_pdf(filename)
        invoice_data = parser.parse_text(lines)
        return invoice_data
