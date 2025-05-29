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
    browser.add_cookie({"name": "MUSIC_U", "value": "0025E407B3B32D7A14ED7E3E8806AB9E73717BBDF6ADE6EC6D992B1591FA61588F9A760FC84298FF4B06165967BC948DDC03C9F03E829597825FD9A0145A74D1A6FDBC4BB67A7AE0DA79E59CFA7C59B9551456ED42C8DC89F1415B9A84C40F2CCB647C9F6C05DC44DE846D450648DA65B5820E26672D6326A840E51EF6212F361594D1935D6E2EC6332FC88F4E0951D071867BBDA1E88D15D30ED9AA9B703F2A4A8D1927BDF193DB1FC149D5D99409DF9EC7223B20CD515F7406619432D4162A451AE4505A24168D5A94074EBBDB520D5A36B4B0C222D7FB3DCBCC2AD5ACF9CD1B1DA1C60A9B5609924BE7CF9BD35407645A884AC96915314F391CD4A8F7A0D10F422F2FD83860C4C3276210E3B8E7A9D942E570F994C7BCC1E290A69F35B6A46A979EA10BADE4607E5AE347B667B7569E29A674E4D9BBA9EBF23DD519A815D6290962BAB189854D9589B852AD1AB05DFB73DD7D7B93B1EC4997ACFF021F5A4F32"})
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
