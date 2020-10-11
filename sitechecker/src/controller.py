from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sitechecker.models import Job


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


def get_html(url):
    main_url = str(url)
    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, "html.parser").text
    text = " ".join([ll.rstrip() for ll in soup.splitlines() if ll.strip()])
    return text.encode("utf-8")


def compareSite(job: Job):
    old = job.html_current.decode("utf-8")
    new = get_html(job.url)
    job.similarity = SequenceMatcher(None, old, new).ratio()
