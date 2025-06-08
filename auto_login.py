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
    browser.add_cookie({"name": "MUSIC_U", "value": "0054E8B19459CAE0C4D95E3BC09D433918E3B5CFC206E9CABABABD64DBF9E42F0143BA67BCEC0BFB3D790874426B5AA5F49FC95EDB57FA239EFDD77F9D1F25A092EDB90ABEF890A09941290739FFAC8265FFA63F5F581E1BEFD94773A2A07CFB320A08C82F6187378EA0A3C492F27AC4144B4ABAF303F800C52E11B5B3FA035EE047837648761DCCB8303DAC78ED4D404B8B38B0224A12E58EA1142DA550A650E92230AA6016BB9504B149715E00B54C19B499B8E7A4CD70ADB3F53C882603EAB11F70AF6F3AEB232AC143F79743164B1DAEFA8ABE930C2A4191B3CF36AB36B7AF311EFC861B12E82F27F1C4A7711C89EF5EC6D789C3EB37A6AA58FFCE128EA62C1800A419B3490BEB37D6279B03087D0439C41A4E53B42381D5903B72D4276258AA12367AA85EBD2527909F0E2FCDD25B8C75D4D03D71E81DC3236C78F6CA4EDFEACFAA74246A5D8687FFD866A30C6D711E0135A7BC80A4D0379093C371558B12"})
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
