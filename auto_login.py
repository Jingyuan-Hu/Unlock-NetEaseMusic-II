# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FC3C44296EA9A6BFFF8439482DC5E58C48EE555170111310F856B88FDB8708785D58FE0FEB490ECE61E1126B2C09B2640344868D1817C53487D8960A101276A4815B6001A8ACBDFA61D66D04B6E5ACC92ACF68A7FE7DA38646802A4D60E4A259FFFE09D276E6D4C9FA24C06B5FE0110AA7C56B300F7FCED788C5515DA8E585EB41D09BFC427927A4ECD296004AE2CB805D520EB0B9AF1C34A9754E11BC980AAC5A459EBB43C67D7F08AF873EC4AF8AD009D73DFD2244592B0B42847AD2BB62310F67B6E44FDC4C0ED8B3029A5E4EC67645935FB212CCB72453BE84F509A117C512CAED68B5E5AF566710A929C333DA7A717C138B10B8468FD8AC41BF712C0A7FD40D2CE40A0688FBBF785AB0C4E565D1A31DFA1D250868EE39286BE0424BDDDD4323E706144D4C8E58C338EB646DD338E0EA1277453543CAEBFF10BD1B3B42C479CE82FBBE23C17519E7A3F456736C3B100E100304FC333B509AE57EA868EAFC56E9CC079C8BE0BCB7CD8354247D3C713753069E1686837BBF04BD3D6E0EF699B759266E6A3F463DF7BC51997FE49F69A7497B5BA09FA6425798E83F4FF78A8A"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
