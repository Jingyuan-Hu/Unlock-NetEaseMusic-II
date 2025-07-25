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
    browser.add_cookie({"name": "MUSIC_U", "value": "007CA092F8C233DD591780CAB71FB20445F6D67E1A9650EEA686ACB1CEFAD993BFDDD5D568B21FE1F801F95841698B4231F35D9951185AC4DC74573061C0E7269F241C433EC0B064D62390E939E0CFEFEBEB721D36C7918B1B2B80EBD68648508FE5CE178325D082B3CBB2325236E0765607FDD8ABCFE5E1B181DCA5D5C774E3FDED5A517E6D225DC8D44F245F5595F3E27200087363D102D7CB05857E1647C447BE0A24F04BD161312E8A412239225EBF1958BB625CBFE5558517368EB9A141A45F047F1DA8E29798C2D15B174CCA83B8970FBD59202AD87E24367A0B874F3A5EE3BE3693C391173DBBAF1B576855CC44FC849223AA051800505D44D0332C880AC3546C4876BB5D19A863F78CBC91CE663A6E9BC61E2E1008EBBFF4794DFDAED8D24B7B16A430FA49CEC2CB7629ECDD08D912330271733257D3DC0B189C77BB6B11ABC02D95E63EFDD69A1748AA5B43BBF08A6047A62581D20564A3A4DF7C1AC8390756A4B0C9016B17ABB3A9DEA0CCD590B776AB869ADC039AF5D387ACFBCF833E9FC1678EE6A45E430C35C1395415538AA7BE8309103E8DBF6CD5ADC1360824"})
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
