from asyncio import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from  pyquery import PyQuery as pq
import os
import time
import pymongo

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 10)

kwd = "iphone"

page = 1

urls = [];

db = pymongo.MongoClient('localhost')['jd']

pages = []

def search():
    try:
        url = "https://jd.com"
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
        #
    except TimeoutException:
        search()

def nextPage():

    try:
        nexts = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.pn-next'))
        )
        next = nexts[0]
        print(nexts)
        # print(next('session'))
        # next.click()
        # next.element()
        # if pages.__contains__(next) == False:
        #     next.click()
        #     pages.append(next)

        # if EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.pn-next.disabled')) == False:
        next.click()




        # #J_bottomPage > span.p-num > a.pn-next.disabled


        # nextPage()
    except Exception:
        print("-----stop------")
        # exit()
        # os._exit()
    finally:
        global page
        # if page == 10:
            # return

        page += 1
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print(page)
        getDetail()

        # nextPage()

def getDetail():


    pages.append(browser.current_url)
    js = "var q=document.documentElement.scrollTop=10000"

    browser.execute_script(js)
    time.sleep(2)

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#J_goodsList')))

    html = str(browser.page_source)
    doc = pq("'''" + html + "'''")
    items = doc('#J_goodsList .gl-warp .gl-item').items()



    print('----------------------------------------------')
    for item in items:
        price = item.find('.gl-i-wrap .p-price strong i').text()
        pname = item.find('.p-name a em').text().replace('\n','')
        pshop = item.find('.p-shop span a').text()
        pcommit = item.find('.p-commit strong a').text()
        pimage = item.find('.p-img a img').attr('data-lazy-img')
        if pimage == 'done':
            pimage = item.find('.p-img a img').attr('src')
        result = {
            'name':pname,
            'price':price,
            'shop':pshop,
            'commot':pcommit,
            'image':pimage,
        }
        saveMongodb(result)
        # print(result)

    allpages = doc('#J_bottomPage > span.p-skip > em:nth-child(1) > b').text()

    currentpage = doc('#J_bottomPage > span.p-skip > input').attr('value')

    if allpages == currentpage:
        return
    nextPage()


def saveMongodb(result):
    try:
        if db['products'].insert(result):
            print("success")
    except Exception:
        print('failure')


search()


