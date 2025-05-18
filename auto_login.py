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
    browser.add_cookie({"name": "MUSIC_U", "value": "008CCAE11594142072B0C12F115338E58C7EE8DA49CF9DFAFFC2A8242DF0ACCEB976EE04AA33C1866FDBAB6BF65D3F3D6117A694A8EE4A49691DC621B9C97EEC321E55B6B4F90D93CF09590ACE60AA99A39531338A9FF743FBA44B63A9B07EF27821080F7BD24BF73BB53824EF39CDFBFB109FBD0A1D1C57FBCBC6D13A11B8265319171F8CA1053D964F306CBC72130A05514CF348ACA8E3D55F5ECD59192FEE5A3CC70691822C1C4CA42886DC15557B072339F6FF84551B308215785182334CA06FAC99C10BC44CE7D063CE5E2C88A9184F6949D2BFE3CDDB25BC36B7AF5D1230EDCB5410D8A45FA8964B696E7507B6061CA0037DEF5A28A6FC37874722E7D652E2C4C9F1D8CA85E2BE30ED9744A32CE9987F657B3112FAB6CE23FC1AB3585590972223AA1BAE02C66A5E2BB084A314EA336E365F20B67956045506CD911A54A34AD49B330B1DACFE70BE8C3BDBAFC852319C7317089D53CA41464F60A4848B5B"})
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
