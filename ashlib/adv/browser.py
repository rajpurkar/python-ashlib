import os
import sys
import re
import collections
import datetime
import time
import threading

import selenium.webdriver

SELENIUM_SEMAPHORE = threading.Semaphore(5)

def read(url, pause=0):
    SELENIUM_SEMAPHORE.acquire()
    
    try:
        browser = selenium.webdriver.Chrome()
    except Exception as error:
        print(error)
        browser = None
    
    if browser is None:
        SELENIUM_SEMAPHORE.release()
        raise Exception("Selenium Chrome webdriver not available.")
    else:
        browser.get(url)
        time.sleep(pause)
        source = browser.page_source
        browser.close()
        SELENIUM_SEMAPHORE.release()
        return source

