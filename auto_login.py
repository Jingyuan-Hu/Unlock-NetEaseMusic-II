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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BE3815297E75610476F34A953E6D05A906D6323CCC6661DA371E8D76F9860F7D1E13C677B35B29BDDE8E864DBA6C00F5D76833BEC11E0C50583ED9918706148F37BB6552F89295237DDFE8F32AC7529A155578323CC07A8A5E72263135F2383B03C640105B0667B6471D1B65F845A47E4CF9F15C2ACA84451BCCDF54F9DCA14AAF00D398DE2ABB062387145C8511055154A555491469D738C6B066825AE2CCDDA296B5EE9649312E46C2BDE672FCF8A70839933F9A428197C2F07467203DCFC07CE95A50BEE1E68B6C1184B6551E5907AB018587E67F3E066C4441D45096387BE0B4B0E80585773E3FE4B0A4D07EEFDA452D4DD7D1677D41E132811A20CF76E62497821DEA059A7C4CCABF582DA3F96307FFD1DBB8009F37118B272348EF78D3A5154DBB89F038ABE76FA0470416E1B1B6910826CA58D3065293540F37F9A7C3A25D79004EB87237365ED8F1A42C42BE0096427BEEF657C13ADD786A549DE828F891896247D3D6289B42380AE425EBDDC46FCA2CDA5175F0D4D4E2978F6118E852D279DAF648BE16BAC7DBB22F10AEF2B6942A75DC22972680643EFACD863613"})
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
