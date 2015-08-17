import os
import sys
import re
import collections
import datetime

import dateutil.parser
from bs4 import BeautifulSoup

def removeWikipediaCitation(text):
    return re.sub("\[\d+\]$", "", text)

def extractLink(linkTag):
    return linkTag.get("href")
    '''if "href" in linkTag.attrs: return linkTag["href"]
    else: return None''' ## TODO: remove if above works
