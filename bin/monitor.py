#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.extend(['../lib/','../conf/']) 
from crawl import WebCrawl2
from mlogger import *
from urls import *

def main():
    web_a=WebCrawl2()
    env=sys.argv[1]
    results=web_a.fetch_parallel(urls_list[env]['asyn'])
    for page in results:
        test=web_a.asyn_parse(page)
        print test
    

if __name__ == '__main__':
    main()
