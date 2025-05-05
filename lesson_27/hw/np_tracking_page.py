import requests
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class NovaPostOpen:
    """ Base NP class to open URL and handle errors """

    def __init__(self, driver, url: str, timeout: int):
        self.driver = driver
        self.url = url
        self.timeout = timeout
        self.open_url()


    def open_url(self):
        # Validate URL format
        if not self.is_url_valid():
            raise ValueError(f"Invalid URL format: {self.url}")

        # Check if the URL is reachable
        if not self.is_url_reachable():
            raise ConnectionError(f"URL is not reachable: {self.url}")

        try:
            self.driver.get(self.url)
        except WebDriverException as e:
            raise WebDriverException(f"Failed to load page in browser: {e}")


    def is_url_valid(self):
        parts = urlparse(self.url)
        return all([parts.scheme in ("http", "https"), parts.netloc])


    def is_url_reachable(self):
        try:
            response = requests.head(self.url, timeout=self.timeout)
            return response.status_code < 400
        except requests.RequestException:
            return False


class NovaPostEN(NovaPostOpen):
    """ Common NP class to fill, click and check EN result"""

    en_input_field_id = 'en'
    en_submit_button_id = 'np-number-input-desktop-btn-search-en'
    response_field_xpath = '//div[@class="header__status-text"]'


    def __init__(self, driver, url: str, timeout: int = 5):
        # Call Base class to open URL and handle errors if exist
        super().__init__(driver, url, timeout)


    def check_en(self, en):
        """ Fill input field with valid EN, submit check form and return 'EN status' text. """

        try:
            en_input_field = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, self.en_input_field_id)),
                message=f'EN input field not found, ID: {self.en_input_field_id}, URL: {self.driver.current_url}'
            )
            en_input_field.send_keys(en)

            en_submit_button = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.ID, self.en_submit_button_id)),
                message=f"EN submit button not found, ID: {self.en_submit_button_id}, URL: {self.driver.current_url}"
            )
            en_submit_button.click()

            response_field = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, self.response_field_xpath)),
                message=f"EN not correct or connection (timeout) issue: {en}, URL: {self.driver.current_url}"
            )
            return response_field.text

        except TimeoutException as e:
            raise TimeoutException(f"{e.msg}")
