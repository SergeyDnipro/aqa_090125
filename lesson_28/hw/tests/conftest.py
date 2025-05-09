import pytest
import logging
from selenium.common import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from lesson_28.hw.pages import HillelQAutoStartPage, HillelQAutoGaragePage
from lesson_28.hw.tests import validate_url


HOME_URL = "https://guest:welcome2qauto@qauto2.forstudy.space/"
GARAGE_URL = "https://guest:welcome2qauto@qauto2.forstudy.space/panel/garage"
SETTINGS_URL = "https://guest:welcome2qauto@qauto2.forstudy.space/panel/settings"

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("test_qauto.log")],
)


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


@pytest.fixture(scope="session")
def browser_driver():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        # driver = firefox()
        yield driver
        driver.quit()

    except WebDriverException as e:
        raise WebDriverException(f"WebDriver error: {e}")


@pytest.fixture()
def homepage(browser_driver):
    return HillelQAutoStartPage(browser_driver)


@pytest.fixture()
def garage_page(browser_driver):
    return HillelQAutoGaragePage(browser_driver)


@pytest.fixture()
def open_page(homepage):
    def _open_page():
        homepage.open_url(HOME_URL)
        logger.info(f"URL opened: {HOME_URL}")

    return _open_page


@pytest.fixture()
def open_registration_form(homepage):
    def _open_registration_form():
        homepage.click_on_valid_element(homepage.START_PAGE_SIGN_UP_BUTTON)
        logger.info("Registration form opened")

    return _open_registration_form


@pytest.fixture()
def fill_registration_form(homepage):
    def _fill_registration_form(name, last_name, email, password, repeated_password):
        homepage.fill_input_field_with_data(homepage.START_PAGE_MODAL_INPUT_NAME, name)
        homepage.fill_input_field_with_data(homepage.START_PAGE_MODAL_INPUT_LAST_NAME, last_name)
        homepage.fill_input_field_with_data(homepage.START_PAGE_MODAL_EMAIL, email)
        homepage.fill_input_field_with_data(homepage.START_PAGE_MODAL_PASSWORD, password)
        homepage.fill_input_field_with_data(homepage.START_PAGE_MODAL_REPEAT_PASSWORD, repeated_password)

        logger.info(f"Filling registration form: {name}, {last_name}, {email}, {password} - completed")

    return _fill_registration_form


@pytest.fixture()
def send_registration_form(browser_driver, homepage, garage_page):
    """ Submit registration form, validate data, log all events. """
    def _send_registration_form():
        user_email = homepage.find_element_silent_mode(homepage.START_PAGE_MODAL_EMAIL).get_attribute("value")
        homepage.click_on_valid_element(homepage.START_PAGE_MODAL_REGISTER_BUTTON)
        user_exist = homepage.find_element_silent_mode(homepage.START_PAGE_USER_EXIST)

        if user_exist:
            logger.error(f"User already exists: {user_email}")
            raise AssertionError("User already exists")

        logger.info("Registration in process...")

        assert garage_page.find_element_silent_mode(garage_page.GARAGE_PAGE_SETTINGS_LINK)
        assert browser_driver.current_url == GARAGE_URL

        # I have used 'send_registration_form' as dict container to pass user details to 'delete_user' fixture.
        send_registration_form.__dict__['user'] = user_email
        logger.info("Registration successful!")

    return _send_registration_form


@pytest.fixture()
def delete_user(browser_driver, garage_page,homepage):
    def _delete_user():
        garage_page.click_on_valid_element(garage_page.GARAGE_PAGE_SETTINGS_LINK)
        garage_page.click_on_valid_element(garage_page.GARAGE_PAGE_REMOVE_ACCOUNT_LINK)
        garage_page.click_on_valid_element(garage_page.GARAGE_PAGE_REMOVE_ACCOUNT_CONFIRMATION_BUTTON)

        assert homepage.find_element_silent_mode(homepage.START_PAGE_SIGN_UP_BUTTON)
        assert browser_driver.current_url == HOME_URL

        logger.info(f"User: {send_registration_form.__dict__['user']} successfully deleted")

    return _delete_user
