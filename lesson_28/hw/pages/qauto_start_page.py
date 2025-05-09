from selenium.webdriver.common.by import By
from lesson_28.hw.pages import QAutoBasePage


class HillelQAutoStartPage(QAutoBasePage):

    START_PAGE_SIGN_UP_BUTTON = (By.XPATH, '//button[text()="Sign up"]')
    START_PAGE_MODAL_REGISTRATION_TEXT = (By.XPATH, '//h4[@class="modal-title" and text()="Registration"]')
    START_PAGE_MODAL_INPUT_NAME = (By.XPATH, '//input[@id="signupName"]')
    START_PAGE_MODAL_INPUT_LAST_NAME = (By.XPATH, '//input[@id="signupLastName"]')
    START_PAGE_MODAL_EMAIL = (By.XPATH, '//input[@id="signupEmail"]')
    START_PAGE_MODAL_PASSWORD = (By.XPATH, '//input[@id="signupPassword"]')
    START_PAGE_MODAL_REPEAT_PASSWORD = (By.XPATH, '//input[@id="signupRepeatPassword"]')
    START_PAGE_MODAL_REGISTER_BUTTON = (By.XPATH, '//button[text()="Register"]')
    START_PAGE_USER_EXIST = (By.XPATH, '//p[text()="User already exists"]')

    def __init__(self, driver):
        super().__init__(driver)

