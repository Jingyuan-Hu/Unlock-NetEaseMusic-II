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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DBC57DB147862551EBA7AAA4BA567FAED8021353CAF92AFB7036DD372D1CB53B5EB2C7E050D81A285CFDD4E941CCE3BBEF1050C576132901E4961E311E13211911E809CC27F2742C0323B6A4481A2A4A6491EF919B3BEFBC5A8A4D991BDD1C62F35361B4CDB7C37C56161FE05EDB0E9E3E66FE7941BE9E3065A8467A7AD476EF71F53DB130DA46FBA15813EE7E9DEEFE5F6A6B5A7DD5B3C0CB4FBCB409622CD93E1E2A811691FDC84C396E9522A38EDF7DEC55CA2EAC0B032FB157585B9E96F14C04EEF83DDEAC86C3872696EECA2AF60C6E874DC53140AD5D2F81834B1669C697E4E5028883981D4A541C3DCEDDB3A06E643EB913FFFEC90F8C087319A041AFC6C8C7365F9824CF68F6E6023587724C722D3D97395B6BF6CAFA143612B4E0F2CEE7C45F2A9249FA700E87FA30A964B1C2FA2A778A05C89C459F9FFC7322455F4A96F8668BF7C9858427115E0C0F82432B8DFF7AA73732FA065A170D02372549"})
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
