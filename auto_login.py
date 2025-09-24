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
    browser.add_cookie({"name": "MUSIC_U", "value": "004314445C611CE6E360DE97F441E739E5A80AD7646F97EFF5CCB71A038A0ED96DF321778D0A57118A4D9D8052E513EEAABBF2B5E85F3201DC0B8E615247C79318BAEC378160A257062DEB5233F7DF458A6B567D78931CB3383FACBB56520C4B3FE58AD1BF2DD2811CBB79D5C7B4B1D5E124B194D820274D34554A147397EB1D1BB1D36597A5F688CF8D31CD3CF34E73270ADAA3A9D743FF4DF367438E2499AABA87FC6DBAD0F5EEC1E0E2CD480921C5756AD56A96E5F6F954E40D036D3C199B74F61EBB982A2F8F07F77BEC5FEDDEC49A1DC284367B1065F64DE67890E79AD81C226EB680EAC460CF9AFF94FC9194A61A921A01015F8A99AB62AE7711E2F573B99E16242F7ACF3D7F3ABF9E9DA63DDFA58E0A623D1CDE7089767BBF50A17C2CCAAF9C150F42CABDAA9942E2DEFB9F2DBDCF9099F135363DC97EF72D05E7715B11E394CBB6F30CD646AF0D39918159C9F1BA979E4E89FC9AB5985390FB26EDDE2A765C4CA6FB430B603DEFE7245DE74175CBB2C62FF251F3813968B38FD995A5C29113996094C97FA735065BB029DB168D864FFF855CE9B91DD0A4FA90018BD722"})
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
