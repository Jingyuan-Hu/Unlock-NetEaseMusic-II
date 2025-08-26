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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A8393C47DF30B71699C66109DDA61728280AE8D37E7F3DECAEF2BDCC594A90CA16307B5111FD4896BEDEC72AE699F6FAADC8A08E6909105720182A72EB556ED3FA51430435160AE12F92DC1BFB35B0994BAE4605E77BAB4D7C109E597CD57CAB887213C80C6DE216504A7A59E79F4112CB9DE8E65956CDEE835FDF1E310203B1234EF3122E120B775A9820D751C30BC1D24AF55560AFC3BC316C2E47B7A7DE057211E4D2FAB99202E2744C28DF107CBA96DD206ED5B1673B5EA9B363963EF94B0E7A0F60A49A9AE3D2BE43E49247DDEAF7EE45E5A2EA0896C64CF3FCD13278D319F31FA48B1BBE81689E02758C5D3D41D3F70CAE714D6774F7E33FBDD8205336F8E7119A976934B1DFBC86DC2AF90A900B145D5D4891BB044160AD752684EC111B0BA694C280FEDED31B90A2D6B993D615AC8EAA9482DBD0B0B95025EA52E2FE46EAE02074CBA18C59926172BE8172384B74EFBE6A751DDB66DD99D00344AB4BB4AC9BFA7091C7D1EE126D38E2252A1BD4AFF82481D7F02BB7EE339392BA1FB6286FBAFC2A032556EBA3C50145633EB2C46B7E205B2644C7D2F548CC245D7119"})
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
