from typing import List, Tuple

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from process import Process, Condition
from utils import parse_price
from process3.const import POPUP_XPATH


EKOBIECA_URL = 'https://www.ekobieca.pl/search.php?text=perfumy'
COCOPANDA_URL = 'https://www.cocopanda.pl/products/perfumy'


class Scraper(Process):
    url: str
    sheet_name: str

    def scrape_products_data(self):
        raise NotImplementedError

    def scrape(self, driver):
        raise NotImplementedError


class EKobiecaScraper(Scraper):
    sheet_name = 'eKobieca.pl'

    def select_products_limit(self):
        select = Select(self.driver.find_element_by_id('select_top_portions'))
        options_number = len(select.options)
        select.select_by_index(options_number - 1)

    def scrape_products_data(self) -> List[Tuple[str, float]]:
        products = self.driver.find_elements_by_xpath('//div[@class="product_wrapper_sub"]')
        products_data = list()
        for product in products:
            name_and_description = product.find_element_by_xpath(".//a[@class='product-name']").text
            price = product.find_element_by_css_selector("span.price").text
            price = parse_price(price)
            products_data.append(
                (name_and_description, price)
            )
        return products_data

    def scrape(self):
        self.driver.get(EKOBIECA_URL)
        self.select_products_limit()
        self.wait(5)
        products_data = self.scrape_products_data()
        return products_data


class CocoPandaScraper(Scraper):
    sheet_name = 'Cocopanda.pl'

    def show_more_btn_click(self):
        load_more_btn = self.driver.find_element_by_id("js-load-more")
        self.scroll_to_element(load_more_btn)
        load_more_btn.click()

    def close_left_popup(self):
        frame = self.wait_for_element(POPUP_XPATH)
        self.wait(1)
        self.driver.switch_to.frame(frame)
        self.driver.find_element_by_css_selector('div.roulette-iframe-close-icon > svg').click()
        self.driver.switch_to.default_content()

    def scrape_products_data(self) -> List[Tuple[str, str, float]]:
        products = self.driver.find_elements_by_xpath(".//div[@class='product-list']")
        self.wait(4)
        products_data = list()
        for product in products:
            brand_name = product.find_element_by_xpath(".//h2").text
            product_title = product.find_element_by_xpath(".//*[@class='product-title']").text
            price = product.find_element_by_xpath(".//strong[@class='price-final']").text
            price = parse_price(price)
            products_data.append(
                (brand_name, product_title, price)
            )
        return products_data

    def scrape(self):
        self.driver.get(COCOPANDA_URL)
        self.wait(1)
        self.wait_for_element(
            'CybotCookiebotDialogBodyButtonAccept',
            By.ID,
            Condition.CLICKABLE
        ).click()
        self.show_more_btn_click()
        self.wait(2)
        self.scroll_to_bottom(scroll_wait_time=3)
        self.close_left_popup()
        products_data = self.scrape_products_data()
        return products_data
