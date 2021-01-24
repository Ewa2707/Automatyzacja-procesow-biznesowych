import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import easygui

from drivers import get_driver
from process import Process
from spreadsheets import StoreDataSheetHandler
from process3.scrapers import EKobiecaScraper, CocoPandaScraper


OPTIONS = ('eKobieca.pl', 'Cocopanda.pl', 'obie drogie', 'żadne')
SCRAPERS = {
    'eKobieca.pl': [EKobiecaScraper],
    'Cocopanda.pl': [CocoPandaScraper],
    'obie drogie': [EKobiecaScraper, CocoPandaScraper]
}


class DataScrapingProcess(Process):

    def choose_store(self):
        user_choice = easygui.buttonbox(
            'Z której drogerii chcesz pobrać dane?',
            'Wybierz drogerię',
            OPTIONS
        )
        if not user_choice:
            user_choice = OPTIONS[0]
        if user_choice == "żadne":
            print("Nie wybrano zadnej z drogerii.")
            sys.exit(0)
        return user_choice

    def automate(self):
        choosed_option = self.choose_store()
        scrapers = SCRAPERS.get(choosed_option)
        for scraper in scrapers:
            scraper = scraper(self.driver)
            data = scraper.scrape()
            sheet_handler = StoreDataSheetHandler()
            sheet_handler.choose_sheet(choosed_option)
            sheet_handler.write_data(data)
            sheet_handler.save()
        self.driver.quit()


if __name__ == "__main__":
    driver = get_driver()
    process = DataScrapingProcess(driver)
    process.automate()
