import logging
from difflib import SequenceMatcher

import requests
from background_task import background
from bs4 import BeautifulSoup
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sitechecker.models import Job

logger = logging.getLogger(__name__)


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
    new = get_html(job.url).decode("utf-8")
    new_similarity = SequenceMatcher(None, old, new).ratio()
    job.similarity = new_similarity
    job.last_checked = timezone.now()
    job.save()
    return new_similarity


@background
def check_job(job_id):
    job = Job.objects.filter(id=job_id)[0]
    diff = compareSite(job)
    if diff < (job.threshold / 100):
        job.last_change = timezone.now()
        job.is_active = False
        job.save()
        user = job.owner
        logger.info("Notify", user.email, job.name, job.method)


@background
def check_jobs():
    try:
        user_jobs = Job.objects.filter(is_active=True)
        if len(user_jobs) > 0:
            now = timezone.now()
            for job in user_jobs:
                if job.last_checked is None:
                    check_job(job.id)
                    continue
                diff = (now - job.last_checked).seconds / 60
                if int(diff) > int(job.check_every):
                    check_job(job.id)
    except:
        logger.error('Something went wrong in check_jobs')
