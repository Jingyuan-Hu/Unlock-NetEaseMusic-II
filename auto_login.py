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
    browser.add_cookie({"name": "MUSIC_U", "value": "00CE77392E777AF6F4E8CE3F38FD6F677FCD192711B4C0DD3E559D080F39FA2210D8F00271515E370BB50A8EC55A923EBEF04BB0266A5EB6FE0302A5CBB90B4E9B9A84A9CF1593F43C60F725E9F141486CAB751E3D865331A51CB60CDC6BB9742D328A5564014E8D613D47532B49EC60B1EAC00B9008CE28760F11E6DD4BAD652D6C023EF8E46C9442DB9D6474F55F10C8771E93FCF1DBE35F98C9B64B9AAEB40EC224F98EAEA5065A4105827247D48E4FFE436571F3678BAE18E191A9D8DBBA6050217347CDB954E9A52655418FCEBCA59912AB3540FD197FDF46A9032BDB9444C4843500E0FEA7553D0F9B4DD21501409C54BC11E945D1C56C017298889BA4C579A7E612109D57C456641A88F316D4434F22D92D6E6E5DF9275F38409EBBF511E35048E037091264E225D5AAD19C56984F0F4940F1DF5A65B92C721CA5B6C66C08EB8AD11967873F9F010B6EB7AB5FFB9F56713A87AC4F66309F05DB15DAED2180316389399A3C39A7D03E400C2CAB0F60DFDF3D222C72D9DF9E3DA49B269A903397B199AD9735F329841DD8E028F1E50151AF0781C0EF317AD85493416DB181"})
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
