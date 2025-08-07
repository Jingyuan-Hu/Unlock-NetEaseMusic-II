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
    browser.add_cookie({"name": "MUSIC_U", "value": "0098D0603BD9A106BC2DFA202A44E5A853C206DD76C1F6CA810D8CCEAB6590A09595DBCAE01BA930D1717719C065AC6E998CE5A706DB3693A15CD5FB6D49C3237918079093A7421D79E653B7E1013F70AAAA787486CB5978E3290D18D7447B8A1548D173397DA072F661D209D417F5B38F35D039DFA8F4293FBFD9FF53818798DEF1B4EF0CDB8735FE6C567CCB0D88F0B87B257D38FD22F705A0AB549FC7CE329143D30D1635CBBD2CCB3D9650B8AFD20D345B365B128909C83237E592C44219719544BFBE0651C62D2E517FE2642E13BDB7D1A37FFEC3558B06B71546D12AB000B4FD3E5FFC460585C3D84852DC9DEDCB131926DDDD3CF7CF5031EFCB6142AC87E4B0D024096F4D57690A4A9FDBB7397F42AF518813A88DC0A8CF4898FD2B4D3A2156B51817423DC65CF413CCF9680D47DEDFC9F42051AFFD8BE8A46C414693ABB945B4E6664F377BFFB49205C77D3A14B9BD8DB71EC052C84D681B6987176529A5A7100191FBBB23F93519CA3903D4B5B40D3078D6F86E63060DD8FC8821AA6839541910F09D8DABB40CFC20F28094C0A8AECB4CC1F8C2C9ACE13A387BABFAA4"})
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
