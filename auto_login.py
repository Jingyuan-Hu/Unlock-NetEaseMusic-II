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
    browser.add_cookie({"name": "MUSIC_U", "value": "001C7A33DBEDC6440B7ACDE4B32975082B44176FAAF458E32EAC654B0536ECDAFD0DD2F7580ABC35B35BCC8B75BAD01127BC3ED1E7C71530260A8DF4D5BCCC06A2E86A01D1A2841C6D126003D448945AEE0292AD310B1E6F1C424884855D672D7C167B629FD6F3C59E12F3A53F32CE345DC75590CCE06189D2A1FD3D79AE19CB20813B40D389DD1ADC5D2D9C79B4DA877CD06FE473B5F008F7367F06C73C027A7A462D848FFEBB25D437A4472383FD7D63B8B46687FA12615BFB78FC6F98F5A1DCDE9B4E80C5DBD5C55DDEA22CBB4E1E682747D4C71B3F2A59ED8BE37CA11A276BD11D305ED0AB10E1DC82AB7BE81A002E403F0444886A770995032A4571D5E42EA61802A75329F608919D004573E43DAD2CC2727AD7A8D667C2A69141913DF4021681CB34EB16D492EF643BBC0D211757BB8342CC5B15D69E074467A4725540A7F0E83AE363BBC22E6502DA7DC25AEC8766104CF2C15CC5CD5FB7AD7173A9FD35123CA4360EEC887349A12315F4086A15"})
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
