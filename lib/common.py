# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4woo'
__github__ = 'https://github.com/bit4woo'

import logging
import sys

def logger():
    LOGGER = logging.getLogger("PassMakerLog")
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

    FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

    LOGGER_HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(LOGGER_HANDLER)
    LOGGER.setLevel(logging.INFO)
    return LOGGER

def strip_list(inputlist):
    if isinstance(inputlist,list):
        resultlist =[]
        for x in inputlist:
            x = x.strip()
            resultlist.append(x)
        return resultlist
    else:
        print "The input should be a list"