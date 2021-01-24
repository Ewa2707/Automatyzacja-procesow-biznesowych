import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from decouple import config

from drivers import get_driver
from employee import Employee
from process import Process, Condition
from spreadsheets import EmployeeDataSheetHandler


URL = 'http://inz.scrapeup.pl/wp-admin/users.php'
USERNAME = config('WP_ADMIN_USERNAME')
PASSWORD = config('WP_ADMIN_PASSWORD')


class AccountCreationProcess(Process):

    def login(self):
        self.wait_for_element(
            ".//input[@id='user_login']",
            By.XPATH,
            Condition.CLICKABLE
        ).send_keys(USERNAME)
        self.driver.find_element_by_xpath(".//input[@id='user_pass']").send_keys(PASSWORD)
        self.driver.find_element_by_xpath(".//input[@id='wp-submit']").click()

    def add_employee(self, employee: Employee):
        # kliknij "Dodaj Nowego"
        try:
            self.driver.find_element_by_xpath(".//a[@class='page-title-action']").click()
            self.driver.implicitly_wait(2)
        except NoSuchElementException:
            self.driver.find_element_by_xpath(".//input[@id='createusersub']").click()

        try:
            self.driver.find_element_by_xpath(".//a[@class='page-title-action']").click()
            self.driver.implicitly_wait(2)
        except NoSuchElementException:
            pass

        # Wypełnij formularz
        self.driver.find_element_by_xpath(".//input[@id='user_login']").send_keys(employee.username)
        self.driver.find_element_by_xpath(".//input[@id='email']").send_keys(employee.email)
        self.driver.find_element_by_xpath(".//input[@id='first_name']").send_keys(employee.first_name)
        self.driver.find_element_by_xpath(".//input[@id='last_name']").send_keys(employee.last_name)
        self.driver.implicitly_wait(1)

        # generowanie nowego hasła
        generate_password_btn = self.driver.find_element_by_css_selector(
            "tr.form-field.form-required.user-pass1-wrap > td > button"
        )
        generate_password_btn.click()
        generate_password_btn.click()
        self.wait(0.5)

        # kopiowanie wygenerowanego hasła
        pw_input = self.driver.find_element_by_xpath(".//input[@id='pass1']")
        generated_password = pw_input.get_attribute('value')
        employee.password = generated_password

        # Kliknij "Dodaj nowego użytkownika"
        self.driver.find_element_by_xpath(".//input[@id='createusersub']").click()
        return generated_password

    def iterate_employees(self):
        employee_sheet_reader = EmployeeDataSheetHandler()
        for row in employee_sheet_reader.iterate_employees():
            employee_data = [cell.value for cell in row]
            if not any(employee_data):
                continue
            employee = Employee(employee_data)
            generated_password = self.add_employee(employee)
            employee_sheet_reader.write_cell(row[-1], generated_password)
        employee_sheet_reader.save()

    def automate(self):
        self.driver.get(URL)
        self.login()
        self.iterate_employees()
        self.driver.quit()


if __name__ == "__main__":
    driver = get_driver()
    process = AccountCreationProcess(driver)
    process.automate()
