import os
import sys
import re
import collections
import threading

from bs4 import BeautifulSoup

from ..util import web

from . import threadpool

def crawl(seeds, pageHandler, linkCondition=lambda link: True, stoppingCondition=lambda processedCount: False, pool=None, priority=0, verbose=False):
    ## TODO: add respect for robots.txt and shit like that
    
    LINK_REGEX = "href\=\"([^\"]+)\""

    seen = set()
    processedCount = [0]
    
    lock = threading.Lock()
    if pool is None: pool = threadpool.ThreadPool(POOL_THREAD_COUNT)
        
    def iteration(link):
        if not stoppingCondition(processedCount[0]):
            page = web.read(link)
            pageHandler(link, page)
            
            for newLink in re.findall(LINK_REGEX, page):
                if web.isRelativeUrl(newLink):
                    newLink = web.extractDomain(link) + newLink

                lock.acquire()
                linkInSeen = newLink in seen
                lock.release()
                
                if not linkInSeen and linkCondition(newLink):
                    lock.acquire()
                    seen.add(newLink)
                    lock.release()

                    pool.put(iteration, args=[newLink], priority=priority)

            lock.acquire()
            processedCount[0] += 1
            pcount = processedCount[0]
            scount = len(seen)
            lock.release()
            
            if verbose:
                ratio = float(pcount) / float(scount) if scount > 0 else 0.0
                print(("Crawled %s pages, %s seen and ratio = %s" % (pcount, scount, ratio)))
    
    for seed in seeds:
        pool.put(iteration, args=[seed], priority=priority)
        
    return pool
    
def sameDomainCondition(seed):
    domain = web.extractDomain(seed)
    return lambda link: web.isRelativeUrl(link) or link.startswith(domain)
