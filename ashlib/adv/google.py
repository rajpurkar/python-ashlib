import os
import sys
import re
import json
import urllib

from ..util import web

def search(query, validLinkRegex):
    urlQuery = urllib.urlencode({"q": query})
    link = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % urlQuery
    response = web.read(link)
    results = json.loads(response)
    hits = results["responseData"]["results"]
    
    for hit in hits:
        if "url" in hit and re.match(validLinkRegex, hit["url"]):
            return hit["url"]

    return None
