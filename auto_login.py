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
    browser.add_cookie({"name": "MUSIC_U", "value": "00179BC512BAA24705EA8987135C4A386C53A36431B7E821ED6046A989FE08C0D7140074CD436E7E753841C3C9CB6E3ED232C04BA7B9EF3B2900DC7A3FF4FFD6940A2B6D2B571129CBBB1FA104249D63ADDE20BB78CC5B716C8C1AF628148A7310C7AA2C1F85DCD388D1FE6C400409C9465B34DEA10A262683314514DB415E022119CD8367A7062B7464BB636BB59E31A7A4D48DB2EF1DD23B7C352E0DE5697D14B0568EECDF9D1E4E6D7087CD64D0A891D5539065D79DF65656008AA8E33009846C5DA104158762BBC13FBF6F9BF3836F501F60B029C21F845D8402E3FC71DF10DABEE15BD48CFE4D2C73204377E9125A49B37B2B5C1D3AB723DE3AF0E0A558DE0460E1B3ACB569AACA21C9B3B7E07BE30CE01A7AB59E90F8526DD760002CDFD71AA8C45826BFB424DD614663B9A20A86D3ADF7FACF3F12B7074F4BEC8FFF9F3BFB3F2CCC26495239C6F5113326EE00DB7AA884DCA2E4C0C4F8CA6A434FFF2EE1"})
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
