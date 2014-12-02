#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os

def log_init(log_path):
	log_dir=os.path.dirname(log_path)
	if not os.path.isdir(log_dir):
		os.makedirs(log_dir)


	logging.basicConfig(
    	level=logging.DEBUG,
    	format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    	filename=log_path + '.log'
	)


if __name__ == '__main__':
	log_init('./logs/spider')
	logging.debug('test file')
	logging.warning('warning test')