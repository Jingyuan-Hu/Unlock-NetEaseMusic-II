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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C3032B21A6262FF8A49F5337D9A18CA7147B8CB9EBE7407943F385B0E43E0695683A57E8A172C597152D59DDB72831D0E8197C0C26948645FB7642A05092BEDA1EAE0F2248B90329F2D5C26E7600320DA99EA3C06921E8FC5D71156FB834AAF069E442307E91825DDD6B08522D5F31A21CD1026C7E1ABDA838C05A24E24CF4AF57EB49A3782F50FF1121182879DC1F8AF34E3FB7FA4B8851909E54CD5D53AE0DA25AF5A33852901A83AD77A5CE35D779F788DDB188AEBA31CEB011EB05333DE3EDB09A0334F0FDCBE9D44BDE3B382D836F6E8B1F3BC454FF90EC887E0A2E14BDD7EC97BC24175ACB81B1E2438566BBEAA30C15DA5CA135390D4225F7D118E4EB31CD75943F0BFE59F0AC81770467B3A939263660B8E6C19C074AFDA161F8B95B293DD883273C54F6EEB6EB1DD856CD6472A26D5741E8174302A83B998E46233EE16BB9E655245CB1EB74B3268E3A52883EA0A78AE76AFC319A3B3B1B4C02C47B97DB45958EAA9F869B6A30EBB6C80CA6657A5A3C770475EF2840DFA8AD2B0138A90EAB347F7211F328B2CFFC077522851CC075B701283D4360117B81390653C4"})
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
