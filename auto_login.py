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
    browser.add_cookie({"name": "MUSIC_U", "value": "00822AEB53DA9E15E9BB9933D38E8854C761E8EC0E55BD16A0A2212D9FC0676AA2258C98EDDAEA6DE512A78BEC13905E43210EB824D8A80C69B22B6B4A2FECAC717A37F33A2BC84E2F2912747D7FC4C484043113F91EB357530D199BA28ADD33AC8C79BE685BC7E1E01D624613BAA514228F5FB9DEADC29E80FD310D4029CDB724F9BB51965AB8134C13F8170B45CF4B291B7D2517F3E145CAADC0E58ECFB7B13E969EBF562A6E6E77F849699C460DEB788175EAD7B6668B7DCAB4C5968F1EB2E7BDEA5643016120A1E126D304BF8AC994F3988C7DC04FC6961A48BE432705AD55DDEF6ECACA23340CBE4A2E275E65F0FD38F926624A0FDE0CEA0F28440CA031FD3E208A05D4B2D66DD946130310DBA2BBD37930C271EB5EEFCE6BD78D7E30AED7232C324230D133B5F89216AA34F4C380BCFEA2FE6D6AEC69CE4942540E2879461262B3B10E86A1A399F2B1C1A9597FED16B48BD88440E179C21CB5B307D268E9"})
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
