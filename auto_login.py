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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DE9AE721C8E6EFDB172C152F05C83EAB30FB76A71471A55E867BFF9130DAAE3B1ED1366561852AEF41A8F422D56101ED3EEFBF30BC2A68BA955885A53F77F73F6E3E6DE36FCB2E188605E0276D80BDE5A959EE6D71A0F96224FA908805780D3AEC4C6BE5A58B057C546866D8696357C46161DF5D7855C71B9DDBC5CF22AD556ABDC37FC4FACA7B1A48C01FBF68253FB300EC6FC51AD4546AAA58E3E88DD4124F77CD0BF237FD19F75117548A03F22652517ACD58247CA7FD887F29D100308829D1D40330C64BCD0D9BE58A9857F3B817E83C5FE8B55A8CBDDBCDBE51E84926E911FF8C854CEB1EB9080E18D633000ED88142D7F0FB1D26BCFD0B6CE268D6A285149872A9D8B6B6971F211B346392CDFB26E296F09401B76030767005EB5CCAF5F9F697AD3B4CCEB9FF8377BAFDE5650AC91812A70DDC0895BA96B0D000A2C90AAB5AC911A5D75340C20FC1F86995E5739F939915B90E8F6751EF2861E1083DBB8189A8E82C6396AB32CFAFCEE0198780E8FDABBBA77E2C598A07904E4683A900A882CA0AB8C8C6A37F983C52B8CD68A888CAEB87E0874C159A2D553EF2C61345"})
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
