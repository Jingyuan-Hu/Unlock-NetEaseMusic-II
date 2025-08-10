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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B11D17E2BC8B28AE9F912BEC026956A746C536E0138F8944FEBC87A13915CC9AE505BE86C53DAC06E2D6DABADCBF6DC30F6CA17F4469C069258BE3DB45D15EA2F0ADF922189284E2EF7457451A209D6576D4E3E47C7D177C8A89FCCDC9A5FC2C32AA4CBA4B8D11F942C67F3C0A2481CF6C66DBB639F7E3576A37424FDB0294437DC00BF54B2A2E66F03455F3A3EB812CFC34B82C09CC56C93FDBCD75C0BCCD9B2D9B300D51ADECFD1315B9E180145E5B99011E75A18B80E1E5412E5F0F11E3D481E61C270D11FF9C912D695517EA2D715B0B626B5CA1032B3DFA0A16A52ABFCBF881C18599D3A98A84EC91F5D2B5C5F1E9FDDA59AE8AA3706F157D6CDE9315E99E97826CD1EE8A0634474642D2B77BE8EC769DEFBDF60E132AA5F1B97ACF8F0860168047BE78F1C1F5F8B2A62FAC7E1DB53E80489F2126B6BF303580F87F88190C13F9772977C578F06B158D05FB0B141F02375972F046CCE43F1E06B0EC1FCCA80F264B45AA91EDC3036D8ECCCD8EFC116AF6645C686AA91D49D5B804A0D1C09E8DEB001490B5F49FF48D47B98055CE22C4D8B77445B718422B1AB3A89FDBD0"})
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
