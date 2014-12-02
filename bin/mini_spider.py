#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,getopt,os
sys.path.extend(['../lib/','../conf/']) 
from crawl import WebCrawl2
import common_conf
from mlogger import *
from urls import *

def usage():
	#使用说明
	print 'Usage of WebCrawl:'

def conf_read(conf_file):
	#参数读取
	import ConfigParser
	cf = ConfigParser.ConfigParser()
	cf.read(conf_file)
	return cf

def file_read(file_path):
	#文本文件读取
	content_list = list()
	with open(file_path) as fread:
		for line in fread.readlines():
			content_list.append(line.strip())
	return content_list

def opt_read():
	opts, args = getopt.getopt(sys.argv[1:], 'hvc:', ['help', 'version', 'conf'])
	for opts, val in opts:
		if opt in ('-h', '--help'):
			usage()
			break
		if opt in ('-v', '--version'):
			print "Persent Version : %s" % common_conf.VERSION
			break
		if opt in ('-c', '--conf'):
			default=CONF_PATH + '/spider.conf'



def main():
	'''
	Mini_Spider 主程序
	'''
	opts, args = getopt.getopt(sys.argv[1:], 'hvc:', ['help', 'version', 'conf'])
	for opt, val in opts:
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
		if opt in ('-v', '--version'):
			print 'Mini_Spider Vesion : 1.0'
			sys.exit()
		if opt in ('-c', '--conf'):
			conf_file = val
			if not os.path.exists(conf_file):
				print 'Illegal conf_file: %s' % conf_file
				sys.exit(1)
			print 'Config_file : %s' % val

	print 'Start Crawling....'
	#参数读取
	spider_cf = conf_read(conf_file)
	urls_list = file_read(spider_cf.get('spider', 'url_list_file'))
	output_dir = spider_cf.get('spider', 'output_directory')
	max_depth = spider_cf.getint('spider', 'max_depth')
	crawl_interval = spider_cf.get('spider', 'crawl_interval')
	crawl_timeout = spider_cf.get('spider', 'crawl_timeout')
	target_url = spider_cf.get('spider', 'target_url')
	thread_count = spider_cf.getint('spider', 'thread_count')
	#print max_depth,crawl_timeout,crawl_interval,target_url,thread_count

	webcrawl = WebCrawl2()
	url_content = webcrawl.fetch_parallel(urls_list, thread_count)
	for page in url_content:
		print webcrawl.url_extract(page)



    
    

if __name__ == '__main__':
    main()
