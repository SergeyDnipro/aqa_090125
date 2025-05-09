from selenium.webdriver.common.by import By
from lesson_28.hw.pages import QAutoBasePage


class HillelQAutoGaragePage(QAutoBasePage):

    GARAGE_PAGE_SETTINGS_LINK = (By.XPATH, '//a[@href="/panel/settings" and text()=" Settings "]')
    GARAGE_PAGE_REMOVE_ACCOUNT_LINK = (By.XPATH, '//button[text()="Remove my account"]')
    GARAGE_PAGE_REMOVE_ACCOUNT_CONFIRMATION_BUTTON = (By.XPATH, '//div[@class="modal-content"]//button[text()="Remove"]')


    def __init__(self, driver):
        super().__init__(driver)