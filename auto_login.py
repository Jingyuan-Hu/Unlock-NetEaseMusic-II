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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DF4A23B9790F3E2A46B6D7F34E3442393A862421D65405803C1EB19AD72DC9462E431E1D05558BF871B953A41C3F3F34CA5CDC208D3D548C7F925CD4C132B2FDFC076AA1B32D3254F38FF30FE0F03308E68E27B4B6A3C7C1461EA5105E0062AEB5646AA0A7A50F970F0AFAE61BBA02807801B09DF6ADF60C66126094A7F9688FC6D9BA3C3BBFA538601F2FA4FE6302F183C19ACF5E963ECD07F82E9565C79ED9913357D7369957DC1316FD134CA805F3A53C632C92A0416FC9B5371E05490BD33C62991F4F2C0832136C43E8D1768530D60A2C49DAC07AE0DAE791979A356050C0F5D29C23EAB7C060B3D972D5F99603A2B813171F7B77FD6853263D8E77C88EA27BE7671E8705FF6708BD0A242E122A015EE3E7044BE40A6A0EF24627B0418AD021327A5589CCC79C1D8AB95EABA9CE39C3D48BDAD908889A221B76E0C581649A57C22F3DD5F9B5FD3CC78259D1947CF694A2E05E1CA9E71342A24A2F2822D3ABEB0E94EF3FF7E794EF34EE7E3B53D5CBD02355B105C7EB3E3C156C1AB78432EF3F4FD53FE0930D14A7DAD3775F692DA35B5F00D122EB1D5B1EAFA48A8B109D"})
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
