class InvoiceParser:
    @classmethod
    def parse_text(cls, lines: list):
        raise NotImplementedError

    @staticmethod
    def sanitaze_data(invoice_data: dict) -> dict:
        invoice_data['invoice_id'] = invoice_data['invoice_id']
        amount = invoice_data['amount']
        amount = amount.replace(' ', '')
        amount = amount.replace(',', '.')
        invoice_data['amount'] = float(amount)
        return invoice_data


class RoboProInvoiceParser(InvoiceParser):
    @classmethod
    def parse_text(cls, lines: list):
        invoice_data = dict()
        lines.pop(0)  # remove "INVOICE"
        date_index = lines.index("DATE")
        address = ', '.join(lines[:date_index])
        invoice_data['address'] = address
        lines = lines[date_index + 1:]
        email = lines.pop(0)
        invoice_data['email'] = email
        date = lines.pop(0)
        invoice_data['date'] = date
        lines.pop(0)  # remove "TERMS"
        terms = lines.pop(0)
        invoice_data['terms'] = terms
        desc_index = lines.index('DESCRIPTION')
        customer_email = lines.pop(desc_index - 1)
        invoice_data['customer_email'] = customer_email
        customer_phone = lines.pop(desc_index - 2)
        invoice_data['customer_phone'] = customer_phone
        customer_name = lines.pop(0)
        invoice_data['customer_name'] = customer_name
        desc_index = lines.index('DESCRIPTION')
        customer_address = ', '.join(lines[:desc_index])
        invoice_data['customer_address'] = customer_address
        first_dash_index = lines.index('-')
        lines = lines[first_dash_index:]
        last_dash_index = 0
        for index, line in enumerate(lines):
            if line != '-':
                last_dash_index = index
                break
        amount = lines.pop(last_dash_index)
        invoice_data['amount'] = amount
        bottom_email_index = 0
        for index, line in enumerate(lines):
            if line.startswith('[') and line.endswith(']'):
                bottom_email_index = index
                break
        lines = lines[bottom_email_index + 1:]
        invoice_id = lines.pop(0)
        invoice_data['invoice_id'] = invoice_id
        customer_id = lines[-2]
        invoice_data['customer_id'] = customer_id
        return cls.sanitaze_data(invoice_data)


class GymInvoiceParser(InvoiceParser):
    @classmethod
    def parse_text(cls, lines: list):
        invoice_data = dict()
        company_name = 'Perfect Gym NOO'
        lines = lines[2:]
        date_issue_label_index = lines.index('DATE OF ISSUE')
        invoice_number = ''.join(lines[:date_issue_label_index])
        invoice_data['invoice_id'] = invoice_number
        lines = lines[date_issue_label_index + 1:]
        company_name_index = lines.index(company_name)
        date = ''.join(lines[:company_name_index])
        invoice_data['date'] = date
        lines = lines[company_name_index + 2:]
        name = lines.pop(0)
        invoice_data['customer_name'] = name
        company_address_beginning_index = lines.index('123')
        address = ' '.join(lines[:company_address_beginning_index])
        invoice_data['customer_address'] = address
        invoice_total_label_index = lines.index('INVOICE TOTAL')
        subtotal_label_index = lines.index('SUBTOTAL')
        price = ''.join(lines[invoice_total_label_index + 2:subtotal_label_index])
        invoice_data['amount'] = price
        return cls.sanitaze_data(invoice_data)


class SaasInvoiceParser(InvoiceParser):
    @classmethod
    def parse_text(cls, lines: list):
        invoice_data = dict()
        lines = lines[2:]
        date_issue_label_index = lines.index('Date of issue')
        invoice_number = ''.join(lines[:date_issue_label_index])
        invoice_data['invoice_id'] = invoice_number
        billed_to_label_index = lines.index('Billed to')
        date = ''.join(lines[date_issue_label_index + 1:billed_to_label_index])
        invoice_data['date'] = date
        lines = lines[billed_to_label_index + 1:]
        customer_name = lines.pop(0)
        invoice_data['customer_name'] = customer_name

        company_name_beginning_index = lines.index('Saa')
        address = ' '.join(lines[:company_name_beginning_index])
        invoice_data['customer_address'] = address

        invoice_total_label_index = lines.index('Invoice total')
        terms_label_index = lines.index('Terms')
        price = ''.join(lines[invoice_total_label_index + 2:terms_label_index])
        invoice_data['amount'] = price
        return cls.sanitaze_data(invoice_data)
