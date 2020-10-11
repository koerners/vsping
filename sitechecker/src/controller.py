import base64
import urllib.parse as urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_screenshot(url):
    if url is not None and url != '':

        CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
        WINDOW_SIZE = "800,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
        driver.get(url)
        screenshot_img = driver.get_screenshot_as_png()
        driver.quit()
        screenshot = screenshot_img
        return screenshot

    return None
