#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,getopt,os

#环境变量初始化
ROOT_PATH = os.path.dirname(__file__)
CONF_PATH = ROOT_PATH + '/conf'
DATA_PATH = ROOT_PATH + '/data'
LOG_PATH = ROOT_PATH + '/log'
LIB_PATH = ROOT_PATH + '/lib'
sys.path.append(LIB_PATH)
import log,utils,logging
import ConfigParser
from crawl import *


def usage():
	#使用说明
	pass
	print 'usage of Mini_Spider:'


def opt_read():
	#参数读取
	opts, args = getopt.getopt(sys.argv[1:], 'hvc:', ['help', 'version', 'conf'])
	for opt, val in opts:
		if opt in ('-h', '--help'):
			usage()
		if opt in ('-v', '--version'):
			print "Persent Version : %s" % utils.VERSION
		if opt in ('-c', '--conf'):
			if not os.path.isfile(val):
				logging.warning("Illegal Config File!")
			else:
				return os.path.abspath(val)
	return None


def main():
	'''
	Mini_Spider 主程序
	'''
	
	log.log_init(LOG_PATH + '/spider')
	spider_conf = opt_read()
	if spider_conf is None:
		logging.debug("No config file input!")
		sys.exit(-1)
	c=WebCrawl()
	#读取抓取配置信息
	ret = c.load_conf(spider_conf)
	if utils.SUCCESS_STATUS != ret:
		logging.error("Load Conf Failled : [%s]" % ret)
		sys.exit(-1)
	#开始抓取
        c.crawl()

	
    

if __name__ == '__main__':
    main()
