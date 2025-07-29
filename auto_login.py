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
    browser.add_cookie({"name": "MUSIC_U", "value": "008EFC4D49CE8B2BF521003D27D6FEC29DA093E73B3F6CA99EB9F4A14DC8E5164C90E30FB67B3EF193D826267AF024DDDC0BCE2C10B7F539BECE04212B5DAEDAE7480EECC178964492AD645997B91A5B02147BFBEF7038EDF88FC1D4C830AF953374BB3086FDB360315F6C5F5E3302EFE8BCD7824BA38048610FD873F38F7C3C306D5B7B7CDF79861376703988DC2C3689EC660F05C0EDCCF3E0E2EA2549B26035BCB5FA3C83B7B9C1E0DA45666C91049EA0BB565311609751BBFFBCE7F359682A344F6F2E41B709E7302A39F552B21192D24788153A76DC539912EF082D66679E84EA9A0FB90D3254A990F798FC9DC8911096D71975DCC01FE7BFCCE9C5CD79F48BAFB669A55375F37A16144234284ED32FEDF81170A301E80AF652CA203C00219C8AFE0F7F93D6A7173C8DC04DE409B803807F771BF07D6AF47860A51C93708C09BB7DBE662618281D02377A097CD4A2043A1B4AE793392DEE9688719412B8CD0FB222737A4CDD2031DF0ED33CB9EB77C3C5D0D69AE4A63EC919033216429560DBA3E1ADECF1E52FA85EFD2B20526C44D5F5CB647079AEF716E78646687B4C13"})
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
