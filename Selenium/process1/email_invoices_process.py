import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from time import sleep

from selenium.webdriver.common.by import By
from decouple import config

from drivers import get_driver
from process1.invoice_reader import InvoiceReader
from process import Process, Condition
from spreadsheets import InvoiceSheetHandler


URL = r'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry = ServiceLogin'
USERNAME = config('GOOGLE_USERNAME')
PASSWORD = config('GOOGLE_PASSWORD')
STACK_OVERFLOW_LOGIN_URL = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27'


class EmailInvoicesSavingProcess(Process):

    def login(self):
        self.driver.get(STACK_OVERFLOW_LOGIN_URL)
        self.wait_for_element('//*[@id="openid-buttons"]/button[1]', By.XPATH, Condition.CLICKABLE).click()
        self.wait_for_element('//input[@type="email"]', By.XPATH, Condition.CLICKABLE).send_keys(USERNAME)
        self.wait_for_element('//*[@id="identifierNext"]', By.XPATH, Condition.CLICKABLE).click()
        self.wait_for_element('//input[@type="password"]', By.XPATH, Condition.CLICKABLE).send_keys(PASSWORD)
        self.wait_for_element('//*[@id="passwordNext"]', By.XPATH, Condition.CLICKABLE).click()
        self.wait(4)

    def get_attachments(self):
        attachments = driver.find_elements_by_xpath(".//div[@class='brc  ']")
        return attachments

    def download_attachment(self, attachment_index: int):
        attachments = self.get_attachments()
        attachment = attachments[attachment_index]
        attachment.click()
        sleep(2)
        download_btn = self.driver.find_element_by_xpath(".//div[@aria-label='Pobierz']")
        sleep(1)
        download_btn.click()
        self.escape()  # zamykamy podgląd załącznika

    def extract_data_from_invoices(self):
        invoice_sheet = InvoiceSheetHandler()
        directory = os.path.dirname(os.path.abspath(__file__)) + "\\invoices"
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                filepath = os.path.join(directory, filename)
                invoice = InvoiceReader.parse_invoice(filepath)
                invoice_sheet.write_row(invoice)
            else:
                continue
        invoice_sheet.save()

    def automate(self):
        self.login()
        self.driver.get('https://gmail.com')
        self.wait(5.5)
        attachments = self.get_attachments()
        for attachment_index in range(len(attachments)):
            self.download_attachment(attachment_index)
        self.wait(5)
        self.extract_data_from_invoices()
        self.driver.quit()


if __name__ == "__main__":
    driver = get_driver()
    process = EmailInvoicesSavingProcess(driver)
    process.automate()
