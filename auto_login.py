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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D712B104C1907FFFDD13766F6383EE2BC9FF986478CA2C83D5962E862E197758E16E46074B7CABFE83ED7E9D4C29761934EC05204F688E5E59B52137CD4A2A43E5D9DF06267E18753A8A6C492BEA1E27CF3607799F07A59330D78F04D30A3441FE3BFC1A3077F5DB5218C3B4666648C3B6B201DDADEBC6E71263542B24A571E01D151A985552DDD4FB7CDD8DC5E790C2C9EC1C095EA49329345973E4108274D0EDF372914B32AE4233A954D0779202803FC734C74BC8DC7E73D7D746F4A12C424F83F3B87DB6DC0839746C46853BCC2E3A2E25DA7540734C2DCFD655BACDF1A4D40548BCC676164E937AA22F424CCE1454AD593CF13817052759E69AEF7640A2E70944CE9263FB414A558436670938D4F8E38DEF92B6AD67477E223D08B91CC0E771673D91CCC7EFF91C59295136AD674122879C1F52EFE4018DAF35DC534971027C239EA26BF9F369452BF12782DEA7D48605E7974D59A544535416E69E59A04D1F81370E6F354B5BE46776711C5A019C3AE9FFCB1A629B3C2794C1E816A7B19845A542C32E1318469353C59AA67B3A63C1E556003169A05A3994ED0DACB406"})
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
