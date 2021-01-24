import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_options():
    chrome_options = Options()
    path = os.path.dirname(os.path.abspath(__file__)) + "\\process1\\invoices"
    prefs = {'download.default_directory': path}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--allow-running-insecure-content")
    return chrome_options


def get_driver():
    CHROMEDRIVER_PATH = '../chromedriver80.exe'
    chrome_options = load_options()
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    return driver
