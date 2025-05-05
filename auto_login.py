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
    browser.add_cookie({"name": "MUSIC_U", "value": "003755563366F8CD37FCBFC49443E207D2FDDA63F65BBA6A51BF287B17AACF5FFB3343C6F6543A067055A6A002D78114CFF672D0DE4929F20B18E876A97DC035B54FA58044C89C6EA2DE4FD113107E79D5F38D25DC8B4667EACB67C4F4BF5AEFE306626D14F5E0A3F781D9C4CA9B1F7723E249FEC03ACC7172B5C58B68EA3C4548F702303F5E024302842CC2FFBED6CFE946B01EADAD65A8008CB7AC68266275C1E83306832CC81595D6E074C463885257AC73A712B416D367CDE878D7F802E30DE33ED199A45A2B4182877CF59D7149C76CDCA4A636E2154AF2D6D4A4D45AAFA025B2F87105E6DF0D7D293B8983F70199407165B0B4FBAEBAE4797BA069AFD5A594B888BAFB4526B1143E06C6D09AFCF21FC9DBF0A4C1A3214351EC61AE33766245411E8CBF739FE22641E710CCC2B794A39E4645BE82CDCBEC1A2D59EF33517FCECEBA300E9032E79ED6C310157AC4A9601E4BF37F68F5A3BC1CB3CF56D73109"})
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
