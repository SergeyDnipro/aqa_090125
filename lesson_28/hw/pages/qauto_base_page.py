from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lesson_28.hw.tests import validate_url


class QAutoBasePage:

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        """ Validate and open URL (by driver). """
        validated_url = validate_url(url)
        self.driver.get(validated_url)

    def find_element_silent_mode(self, locator, timeout: int=2):
        """ Find element with no raising errors on exception. Return False on exception."""
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            return False


    def find_element(self, locator, timeout: int=5):
        """ Find element by 'locator'. """
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}, URL: {self.driver.current_url}")


    def wait_to_be_clickable(self, locator, timeout: int=5):
        """ Wait until the element will be ready for click. """

        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except:
            raise TimeoutException(f"Element not clickable: {locator}, URL: {self.driver.current_url}")


    def click_on_valid_element(self, locator, timeout=5):
        """ Click of valid element. """
        element = self.wait_to_be_clickable(locator, timeout=timeout)
        element.click()


    def fill_input_field_with_data(self, locator, data):
        """ Fill input field founded on 'locator' with 'data'. """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(data)
