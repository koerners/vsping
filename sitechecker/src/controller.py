import urllib

from html_similarity import similarity
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sitechecker.models import Job
from sitechecker.templatetags.sitechecker_extra import bin_2_img


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


def compareSite(job: Job):
    fp = urllib.request.urlopen(str(job.url))
    html_bytes = fp.read()
    sim = similarity(bin_2_img(html_bytes), bin_2_img(job.html_current))
    job.html_current = html_bytes
    job.similarity = sim

    return sim
