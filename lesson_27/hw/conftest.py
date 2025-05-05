import pytest
from selenium.common import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver


def firefox(debug=False):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox() if debug else webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver


def chrome(debug=False):
    options = ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome() if debug else webdriver.Chrome(options)
    return driver


@pytest.fixture()
def browser():

    try:
        driver = firefox()
        yield driver
        driver.quit()

    except WebDriverException as e:
        raise WebDriverException(f"WebDriver error: {e}")