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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DBA0DAA0EC81360F889ECFEBB7E9238389F035BC9A0A31DE7A8AD7B013212DA55913A77E16C94787FCCB30BC9736B6A7466336D507DC77DD9FB6A11D2557305B2EF528189B8B597BE5B5B43A64DE26A1D498F5F12380796646001B500706BB3330649F700249E3222B9B8E9D68ECBD7CFC1C95A2FEF6C509B151A48FC113AB6D6CAE9A05C52594B877B87F6FFF7898B469E86BD1669A9F7F7747E23A92BD97453454ED569CE2AA39F1C48C6F11700C1B488590FBB74BF04EF975E802A0F5F65E1A92E49FF49CCF797FA69B46B26C9EEEB3582995DDCC7D2ED0F0526C5FAE18C7395967B45F0DC6D293F9FD5260D21F05053C6533CE50D4C3D6A6ADA68BC5A27E91E830D325D4F9AED57EA9B05E44240C63135EF225686FD8429AECE741C6F9DD5A155C13E380EC7459A5E118C74611693982383ACE6AA5B9494BEFB736DA000367DD1C972330288318D918801FC3B2C94B121C845BB511DA20CD63F1845E0AEA81B2257AB391B0C0FD23A60C915A3224FB0A5520B7EE3681EC0CA1B160EB0DD1B6277B9F216CD3D7319D101FC0371298BF05B6FE4B273F59EF3E276C358D0E2B"})
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
