from asyncio import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from  pyquery import PyQuery as pq

import pymongo

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 10)

kwd = "iphone"

page = 1

urls = [];

db = pymongo.MongoClient('localhost')['jd']


def search():
    try:
        url = "https://jd.com"
        print(url)
        browser.get(url)
        # global wait;
        inputs = wait.until(
            EC.presence_of_all_elements_located((By.ID, "key"))
        )
        input = inputs[0]
        input.send_keys(kwd)
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > div.form > button'))
        )
        submit.click()
        getDetail()
        # nextPage()
    except TimeoutException:
        search()

def nextPage():

    try:
        nexts = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.pn-next'))
        )
        print(browser.current_url)
        next = nexts[0]

        next.click()

        # nextPage()
    except Exception:
        print("-----stop------")
    finally:
        global page
        if page == 10:
            return

        page += 1
        print(page)
        nextPage()

def getDetail():

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#J_goodsList')))

    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-warp .gl-item .gl-i-wrap').items()

    for item in items:
        print('------------------------------------')
        pname = item.find('.p-name').text()
        saveMongodb({'dex':pname})
        print(pname)


def saveMongodb(result):
    try:
        if db['products'].insert(result):
            print("success")
    except Exception:
        print('filure')


search()


