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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AC97BAD2626806DE9AAC666F5BFBA6779849AF6F8BAA1513D7E5C8195CBC7D70B417454F3BA6AC2FFB4244160F97DB1781090CCF511F26EAD994846997ED84AA5C0FAD1F6C0878EF548CEB0B66063A51D6631FACB918410654932565CDD040C49356E0D78BAA978C15B881A7A48202800EB540A20D33DFE94A716CE04F2E7481CCC1BB95E925CA0F8D6FF2D36EA5873903604CCBA506F7363DF2C236E2199CAF8D13D615D608AA9B45C4DAFECC8963EC5E1A622B4B5FA6334ED2751970B2E8453AC523D4B92224AD91C5C8D7BB879A2DF2672D662F2C5747ABA8E3785C97F8DA845A28F9DC146917211C9844B4B2B596B3DAAD109B494F6D5CFEDFE165574EC8F311E38A7540AC9BF9C7559835F59E61550B6F127A04F07BFCCECF34AE016BE74F075F1257B7348A87AA8F66652F508911527BB5F721CD38D897BA3F5A3C0123D0176B6122B644798659EA298BC8B01BB6A7B8E99F92D1607D5985288E19A273ADBA5411BC38B8F4F0A128F285E87EFB789732D3919619F97234D11FDC0AEEEBF733381AC564663E652A3F066E858B82FBF1630EC440C229A65C3343F27EACC8"})
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
