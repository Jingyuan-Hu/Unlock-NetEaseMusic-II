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
    browser.add_cookie({"name": "MUSIC_U", "value": "008FB4E4500403E1780842BF59EE07BF7EC64EA737A6D33D0AF5AAFC2F4930BBF59559FC2BF8F612757ACF2E4167E9CC00766CB477D99349829110387754ECED011090F8ED960AED8FF0BE31E7B2C36F298C87E5DF5F91DBE614B59F7C23630B217143D4D155C600B781347CE901FE1456F55592DCF0883E75D0C26506FC5F097F57D01CAE3B08B1C8FF1F05E57DF430F46C45A6C079680A56F344DB9C97495A8D6F79B599230806A21BC586A07D82CFBDF150FB037A9B32CB51141FC95AE0BD763E0B0AB50F374537767B87C526A51F1DCC5F00418DA15CBC270094B8CC84B4F64C1E0171BFBFB6B2615EAF20292F3BEA0A9A9BDDDB8C879DC2F8F7D9FDB940DD70EB5EDF50BD4A1489660E1981BF7DAF56851A1BBDE667DA6DB9DC23C80E9844BCB613FBCCA5918B8155D5C2D70F8A2BD00C61964DC990952855CBE8457D3902486FA8CFABA97585F32362F27A52D672DFD68A2C3256FECD7E724A9465112EBF4FB66E7DB695A0A0A211FB49E666F22D2B9C1BCD3AEA11B9249674D82007E8F2E0EA007B7DE6E50B566AD680F5D413F6295E139B5CA0DE39BE40EBB0D27723B7"})
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
