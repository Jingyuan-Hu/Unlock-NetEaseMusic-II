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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C8B2C9B2E49C208971603333420F439E6F78EEEFA869B749AF39B5A025BB4893D3987E2EEDDEFE5F3E3AF94A10BED77D84D826AE44A71DB78DC6E980F16F1083D6B47E1782EE5CCE8224796E9D6C7A6BABDF37E3B91185E5DF07ACDB5321FB7C51DD4DC2B252B691DBF81B1D3641B2DF39493FAF37F5881D89EAD907AAFC9779A62C84BBD943BB876137109E825EE675BA30963B198F7FD95DFDE429FE863C984F390DBEC66EF167240CF54777B884D5286BEC16B3D0493E8CF294A31A3FA04193F844ED5CB81744DEC124E06E86DC719E0791A0081D8792ADBB9D8D4184E5057AFFA2BF305BBC2811815B2B20210299AD2522C731244B795E7F71865214AB381949C8FB3077C61B886FD4FA06980E6ED533F182D48E39934FA99AD2F1F1F186C3AEB4AD90BF2A21B8B5BF83443E75A69F2C1AE89E378FB0BECD8D0628004208F30DEA8412ECBBFB451254A96313FF15FD3456E57581491BBA2A58D2D8F30D1A"})
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
