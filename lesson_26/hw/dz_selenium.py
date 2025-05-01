import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from logging_formatter import CustomFormatter


# Initiating logger configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('check_frames.log')
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)


def search_and_check_frames_for_correct_input(url:str, correct_answers: list[str]):
    driver = webdriver.Firefox()
    driver.get(url)

    # Search frames in HTML file
    frames = driver.find_elements(By.TAG_NAME, "iframe")

    for frame_index in range(len(frames)):
        frame = frames[frame_index]

        try:
            # Get current frame instance and secret phrase to input
            password = correct_answers[frame_index]

            # Switch to frame from main window
            driver.switch_to.frame(frame)

            driver.find_element(By.TAG_NAME, "input").send_keys(password)
            driver.find_element(By.XPATH, "//button[text()='Перевірити']").click()
            time.sleep(1)

            # Get text and process Alert window
            alert = Alert(driver)
            alert_text = alert.text
            alert.accept()

            if alert_text == 'Верифікація пройшла успішно!':
                logger.info(f"URL:{url}, Frame:'{frame.get_attribute("id")}' - Verification PASSED!")
            else:
                logger.info(f"URL:{url}, Frame:'{frame.get_attribute("id")}' - Verification FAILED!")

            # Switch back from frame to main window
            driver.switch_to.default_content()

        except Exception as e:
            logger.error(
                f"During processing URL:{url}, Frame:'{frame.get_attribute('id')}' - exception occurred: {e}",
                exc_info=True
            )

    # Close browser
    driver.quit()


if __name__ == '__main__':
    url = "http://localhost:8000/dz.html"
    correct_answers = ['Frame1_Secret', 'Frame2_Secret']
    search_and_check_frames_for_correct_input(url=url, correct_answers=correct_answers)
