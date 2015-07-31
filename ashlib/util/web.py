import os
import sys
import requests
import urllib
import logging

import str

logging.getLogger("requests").setLevel(logging.WARNING) ## TODO: move elsewhere?

def read(url):
    return str.sanitize(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text)

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
