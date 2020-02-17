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

def hasSpecialchar(string):
    if string is None or len(string) == 0:
        return False
    for x in string:
        if 32 <= ord(x) <= 47 or 58 <= ord(x) <= 64 or 91 <= ord(x) <= 96 or 123 <= ord(x) <= 126:  # 特殊字符
            return True
    return False

def hasNumber(string):
    if string is None or len(string) == 0:
        return False
    for x in string:
        if 48 <= ord(x) <= 57:  # 数字
            return True
    return False

def hasUpperletter(string):
    if string is None or len(string) == 0:
        return False
    for x in string:
        if 65 <= ord(x) <= 90:  # 大写字母
            return True
    return False

def hasLowerletter(string):
    if string is None or len(string) == 0:
        return False
    for x in string:
        if 97 <= ord(x) <= 122:  # 小写字母
            return True
    return False