from enum import Enum
from time import sleep
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Condition(Enum):
    CLICKABLE = "clickable"
    VISIBLE = "visible"


CONDITIONS = {
    'clickable': EC.element_to_be_clickable,
    'visible': EC.visibility_of_element_located,
}
MAX_ELEMENT_WAIT = 20


class Process:

    def __init__(self, driver):
        self.driver = driver
        self.url: str = None

    def escape(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()

    def scroll_down(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def wait(self, time_to_wait: Union[int, float]):
        sleep(time_to_wait)

    def wait_for_element(
        self,
        selector,
        select_method=By.XPATH,
        condition=Condition.VISIBLE
    ):
        condition = CONDITIONS.get(condition.value)
        element = WebDriverWait(self.driver, MAX_ELEMENT_WAIT).until(
            condition((select_method, selector))
        )
        return element

    def get_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def scroll_to_bottom(self, scroll_wait_time: Union[int, float] = 3.0):
        height = self.get_height()
        while True:
            self.scroll_down()
            self.wait(scroll_wait_time)
            new_height = self.get_height()
            if height == new_height:
                break
            height = new_height

    def scroll_to_element(self, element):
        desired_y = (element.size['height'] // 2) + element.location['y']
        window_h = self.driver.execute_script('return window.innerHeight')
        window_y = self.driver.execute_script('return window.pageYOffset')
        current_y = (window_h // 2) + window_y
        scroll_y_by = desired_y - current_y

        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

    def login(self):
        raise NotImplementedError

    def automate(self):
        raise NotImplementedError
