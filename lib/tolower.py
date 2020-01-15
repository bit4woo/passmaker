# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4woo'
__github__ = 'https://github.com/bit4woo'

list = open("passmaker-2017-11-03-15-49.txt").readlines()
result = []
for item in list:
    x = item.lower()
    result.append(x)

fp = open('english_name_with_chinese_last_name.txt',"w")
fp.writelines(result)