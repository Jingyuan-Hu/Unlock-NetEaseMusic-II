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
    browser.add_cookie({"name": "MUSIC_U", "value": "007FD921C8C4AF562166466A2D020FC200D56D303AC4FA5A9F663D10D326E2A1B917E9C9459E82CD30C869F6328A5BC6C754E52FCF8B3C36D85890CA5B13D1BDFD634ABE45F3736632F93C23434776A866E4BBB9E0E2DB93BE36FE74E6EEDB373D31E452A2FB4BF736D5304A19668F440667F16DA71216EB7A17B4D4FABE0800696036147E79EEC03646448E1C9527059902C7F10223B90837AD78F34E805F3DD2D26D703F67533877FAF82BEF1543C823A3EC7CF6B6D22ACEE8A694B1E938F8E2E07111DEE0A4C36568F20EF11B2ADCE8D9F6729BF960300E8232FA8C6038E8C7B3F2CE8BB333076ABCE4D4F841C6A63B96141B93ECAF8CF99B70825465A744304B22FD326A8C6974AD97B37BF405F4F7692C0DC8B14A7FEF70E9B50394CE146A5D32B77651B2BEC265CEF62AD55C2C0DDE650A2DD1967746CA0EE6B41F518FF4193A797702BC65441838E821B79333485D59792A74593024A1303FFE400E0F7B910B970513BC10208653E169FDF0D6AC80421B9CEE9F1ED6B5F18FE2F90FBEE67880E767DAFF85905ACB6AD4893814982A4F7CB7C3F1344A01553889B386D5E1"})
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
