#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,urllib2
import sys,time,os
import log
import logging
import ConfigParser
import utils
import chardet
import gzip
import zlib
from bs4 import BeautifulSoup


class WebCrawl:
    def __init__(self):
        self._conf_dict={}
        self._url_list=[]

    def _int_para(self, conf, conf_dict, para_list):
        '''
        整数类参数读取
        '''
        for para in para_list:
            if conf.has_option('spider', para):
                try:
                    conf_dict[para]=conf.getint('spider', para)
                except ValueError:
                    logging.warning('Need Intval Input')
                    return utils.ERROR_INVALID_INT_CONF
        return utils.SUCCESS

    def load_conf(self,conf):
        '''
        参数读取
        '''
        import ConfigParser
        conf_dict={}
        spider_conf=ConfigParser.ConfigParser()
        spider_conf.read(conf)
        if spider_conf == []:
            logging.error("Spider_Config is Empty!")
            return utils.ERROR_INVALID_CONF
        if spider_conf.has_option('spider', 'url_list_file') \
            and os.path.isfile(spider_conf.get('spider', 'url_list_file').strip()):
            conf_dict['url_list']=spider_conf.get('spider', 'url_list_file').strip()      
        else:
            logging.warning("URL List File Not Exists [%s]" % spider_conf.get('spider', 'url_list_file'))
            return utils.ERROR_INVALID_URL_FILE
        if spider_conf.has_option('spider', 'target_url'):
            conf_dict['target_url']=spider_conf.get('spider', 'target_url').strip()
        ret=self._int_para(spider_conf, conf_dict, ['max_depth', 'crawl_interval', 'crawl_timeout', 'thread_count'])
        if ret != utils.SUCCESS_STATUS:
            return utils.ERROR_INVALID_CONF
        self._conf_dict=conf_dict
        return utils.SUCCESS_STATUS

    def _read_urls(self):
        '''
        读取种子url
        '''
        try:
            with open(self._conf_dict['url_list_file']) as fread:
                for line in fread.readlines():
                    self._url_list.append(line.strip())
        except IOError as e:
            logging.error("Load Url File Failed, Error: %s" % str(e))
            return False
        return True

    def _deflate(self, data):
        try:
            return zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            return zlib.decompress(data)

    def check_zip(self, resp):
        '''
        判断是否为压缩网页
        '''
        if resp.headers.get('content-encoding') == 'gzip':
            data=resp.read()
            unzip_data=StringIO.StringIO(zlib.decompress(data, 16 + zlib.MAX_WBITS))
            new_resp=urllib2.addinfourl(unzip_data, resp.headers, resp.url, resp.code)
            new_resp.msg=resp.msg
            return new_resp
        elif resp.headers.get('content-encoding') == 'deflate':
            data=resp.read()
            gz=StringIO.StringIO(self._deflate(data))
            new_resp=urllib2.addinfourl(gz, resp.headers, resp.url, resp.code)
            new_resp.msg=resp.msg
            return new_resp
        else:
            return resp

    def crawl_page(self, url):
        '''
        抓取url内容信息
        '''
        headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2; rv:7.0.1) Gecko/20100101 FireFox/7.0.1',
            'Accept-Encoding' : 'gzip, deflate',
            'Content-Type' : 'application/x-www-form-urlencoded',
            }
        try:
            req=urllib2.Request(url, headers=headers)
            resp=urllib2.urlopen(req, timeout=self._conf_dict['crawl_timeout'])
            if resp is not None:
                resp=self.check_zip(resp)
                data=resp.read()
                encoding=chardet.detect(data)['encoding']
                if encoding == 'GB2312':
                    encoding='GBK'
                if encoding == '':
                    encoding='utf-8'
                data=data.decode(encoding)
        except (urllib2.HTTPError, urllib2.URLError, \
            httplib.HTTPException) as e:
            logging.error('Url %s Crawl Failed Error [%s]' % (url, str(e)))
        return data

    def _parse_url(self, base_href, url):
        '''
        处理抓取的url，返回完整url
        '''
        from urlparse import urlparse,urljoin
        url_info=urlparse(url)
        if url_info.scheme is None:
            tmp_url=urljoin(base_href, url)
            return tmp_url
        else:
            return url

    def _get_urls_from_a(self, url, base_href, soup):
        '''
        从a标签抓取链接
        '''
        links = []
        a_list = soup.findAll('a')
        for a_tag in a_list:
            link = a_tag.get('href')
            if link is None or len(link) == 0:
                continue
            if link.find('javascript') >= 0 and link.find('href') < 0:
                continue
            url=self._parse_url(base_href, link)
            links.append(url)
        return links
    
    def _get_urls_from_img(self, url, base_href, soup):
        '''
        从img标签抓取url
        '''
        links=[]
        img_list=soup.findAll('img')
        for img_tag in img_list:
            link=img_tag.get('src')
            if link is None or len(link) == 0:
                continue
            url=self._parse_url(base_href, link)
            links.append(url)
        return links

    def get_urls_from_page(self, url, data):
        '''
        从页面抓取url主程序
        '''
        links=[]
        if data is None:
            return False
        soup=BeautifulSoup.BeautifulSoup(data)
        base_href=''
        base_tag=soup.find('base')
        if base_tag is not None:
            base_href=base_tag.get('href')
        links.extend(self._get_urls_from_a(url, base_href, soup)
        links.extend(self._get_urls_from_img(url, base_href, soup)
        return links

    def mini_spider():
        '''
        多线程广度优先抓取
        '''
        pass
        



    def sync_parse(self,content,desc):
	    pass

    def asyn_parse(self,content):
        import simplejson
        result=simplejson.load(content)
        return result.keys()
    def code_crawl(self,url,try_times=3,sleep_time=0.2):
        for i in range(try_times):
            code=self.get_code(url)
            if content == 200:
                return content
            else:
                time.sleep(sleep_time)
                continue
        logging.debug('Bad Url: %s' % url)
        return code

    def fetch_parallel(self,list_of_urls,pool_num=4):
        '''
        并行抓取
        '''
        from multiprocessing.dummy import Pool as ThreadPool
        pool=ThreadPool(pool_num)
        results=pool.map(self.content_crawl,list_of_urls)
        pool.close()
        pool.join()
        return results

    def url_extract(self, web_content, url_regex=''):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(web_content)
        all_links = soup.findAll('a')
        return all_links


    def fetch_code_parallel(self,list_of_urls,pool_num=4):
        from multiprocessing.dummy import Pool as ThreadPool
        pool=ThreadPool(pool_num)
        results=pool.map(self.get_code,list_of_urls)
        pool.close()
        pool.join()
        return results
        

def main():
    webcrawl=WebCrawl()
   # print webcrawl.url_read(sys.argv[1])
    env=sys.argv[1]
    results=webcrawl.fetch_code_parallel(urls_list[env],12)
    #for url in urls:
    #    tmp=webcrawl.content_crawl(url)

if __name__ == '__main__':
    main()
