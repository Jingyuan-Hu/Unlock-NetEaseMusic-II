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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A0331E17177C6D3FA56456C841AB54CA5F0DDDCBB78A812F2C0A518BF6619915D30119D5B2C3EDEEB31F98B18DE7761E514F8C2828290D9763986E476785437CA0F5631C0AFE57B809FFB071718D1F6075E107359FFF001139E894E7B0C0438646BC7F5C467088AC5A837976E705D77414AFFF0BBD79BE703E6820B7F8549129FAEABA9670977D819D49C38E1B90BD6BC5608CB8FA705C6C2FF5FC96590E39B2EB3772971C54167512909CC8B43DBFFF9D1F7E23CD2082F12B2A08A9391FE5012909DFC605D440D13911A1BAFA82BDB76E0AAC00EF40C72E1E098B2D47E1E59933F3066AE899F9485AAD8799ABD39638BF44CBF4305DFB3792070DE176FA6E5B89A6BDB5F494B745271AC6869719E5F962D9DCBE23F5B3B543133ABDB4F70BD54331546A8C0AAE9253B42903F463631DA537D443F921ADC544AD53FCCF089FFDC1D3E4E9E175DF3434D5E60A77609702DB52F24651160BC85AA69A2B1655E4FE"})
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
