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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C6C5920A0B818A722C405303D005C6424733889D70F698E92B92BC2F5C2F7390CF09B83F42197ADAD995603E11163E739149548A3CD7F2C31DCE5C13AFE97AD481DE13404F625446D0D83A7962280A85B1BA5AAEF929749B4141B6A4E5DADC7777EB9840BD9A0B1B8BF1AF49578D81113A80D74C5320397187FB878B980587F2590E389A47661B926DC0E86F4CCAD5B066E881B37B5173AE10B1B558803248C5B54C9C46DF089B9ECB29BDCD3D9AE787F1968F3FC14841ABD7AE0AC327F7B221F93B24777987A4014357A1C33C93A71C9FF40E77AA0FDFCA69CAEB3FA7BDCC29ACBD94998AE91A2C2A56C346EB39E5D2A934518A708E954BE7F1DD877A1B48950E64E53BE54199DC84C03587980BBD42605B72ADD6E06585D8DF886905CCCEFE25826C067A0E31D1767A984A03DEA2D84BB464798AAF41DC13F5F1AD3C1F99CDF68BCDAD353184BAB5C29C415C469D221789932CBB1B11F0AC44E86CC86B1BAEC805183A9B610296AA9D46088E67FB3EED25F06295F6C726D4705D68BC626A5A06A729E40DAE05EFAC9CF40BBED8EA8B1C252125E1C51AA4A451CCEC5A5058F1"})
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
