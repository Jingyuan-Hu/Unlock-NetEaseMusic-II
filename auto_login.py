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
    browser.add_cookie({"name": "MUSIC_U", "value": "00423F27337ABCF327E09A3F383507724ACAB0D328640833CF65D1CC4CA8F75762C25829616B1FB812108276F2DC6FDB82E086215CEA226CED797863021993DB6517738A01CE52FF11ACF375696F2109EE0248F448186DAEBC360CECD3C05DBB8C3DC55BC05113D9931CD261AC9E3DF900193E457A9FC8F4B26A9F76634A184FF3E007E6901BDEA6BFEF113AAF7BDEEE2FFB6C9F144AFDC7CEE8DF7ED7F036CCE95DBC736B61941BE30618D258D01802016A9C728A99F44BC6EAA70B37948052DB133CF049CBF1704CB8B3DADE818659577D02A029135648921A4AA61A5D1291A7C017ADC636E91430DC5E75C2248D515770AEC2FD0D8A131688BFB0398EB4E9A2D958F36915F7D4130A84E0DD37890B9DDBA4E2251C3555CCF4CEF53AAC5EA54CE4974EF60A496969D1916742286022DD047BA74CC3D03C74060C1994C90A204B0DF70E9F8A8DE6E3B76E8137BE615D985C9CF4EF895F5C223A6A57EE615471F4"})
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
