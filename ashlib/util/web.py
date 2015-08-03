import os
import sys
import requests
import urllib
import logging
import time

import selenium.webdriver

import str_

logging.getLogger("requests").setLevel(logging.WARNING) ## TODO: move elsewhere?

BROWSER = selenium.webdriver.Chrome()

def read(url, headers={}):
    headers = {"User-Agent": "Mozilla/5.0"}.update(headers)
    return str_.sanitize(requests.get(url, headers=headers).text)

def readViaBrowser(url, pause=5):
    BROWSER.get(url)
    time.sleep(pause)
    return BROWSER.page_source

def overwrite(filePath, url):
    file = open(filePath, "w+")
    file.write(read(url))
    file.close()

def extractDomain(link):
    endIndex = link.find("/", link.find("//") + 2)
    if endIndex == -1: return link
    else: return link[:endIndex]

def isRelativeUrl(link):
    return len(link) > 0 and link[0] == "/"


