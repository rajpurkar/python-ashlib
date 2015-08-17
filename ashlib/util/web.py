import os
import sys
import requests
import urllib
import logging
import time
import threading

import str_

logging.getLogger("requests").setLevel(logging.WARNING) ## TODO: move elsewhere?

def read(url, headers={}):
    headers = {"User-Agent": "Mozilla/5.0"}.update(headers)
    return str_.sanitize(requests.get(url, headers=headers).text)

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

def html2xml(html):
    html = html.replace("&apos;", "'")
    html = html.replace("&quot;", "\"")
    html = html.replace("&amp;", "&")
    html = html.replace("&lt;", "<")
    html = html.replace("&gt;", ">")
    return html
