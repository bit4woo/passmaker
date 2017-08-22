# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import config
import inspect
import itertools
import datetime
import os
import sys
import logging

def logger():
    LOGGER = logging.getLogger("PassMakerLog")
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

    FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

    LOGGER_HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(LOGGER_HANDLER)
    LOGGER.setLevel(logging.INFO)

    return LOGGER
logger = logger()
def getseedname():#获取所有list
    result = []
    for item in inspect.getmembers(config):
        if isinstance(item[1],list):
            #print item[0]
            result.append(item[0])
    #print result
    return result

def getseedvalue(name):
    for item in inspect.getmembers(config):
        if name == item[0]:
            #print item[1]
            return item[1]


def passmaker():
    logger.info("making password ...")
    now = datetime.datetime.now()
    timestr = now.strftime("-%Y-%m-%d-%H-%M")
    filename = "passmaker{}.txt".format(timestr)

    resultlist = []
    templist = []
    rulelist = []
    for item in config.rule: #所有规则
        if config.keep_in_order == False:
            x = item.split("+")
            y = len(x)
            z = itertools.permutations(x, y)#结构是list,
            rulelist = list(set(z))#一个规则变成了多个
            #print rulelist
        else:
            rulelist.append(tuple(item.split("+")))
            #print rulelist

        for item in rulelist: #item 是一个规则
            #print item
            try:
                for i in item: #解析一个规则，i是seed,单个组成部分
                    if i in getseedname(): #seed 是否有在config中定义
                        if len(resultlist) == 0:
                            resultlist = getseedvalue(i)
                        else:
                            for x in resultlist:
                                for y in getseedvalue(i):
                                    templist.append(x+y)
                            #print resultlist
                            resultlist = templist
                            templist = []
                    else:
                        #print "No \"{0}\" found in config.py,Please check".format(i)
                        raise Exception("No \"{0}\" found in config.py, Please check your config!".format(i))

            except Exception,e:
                print e
                exit(0)
            #begin write file
            fp = open(filename, "wb")
            for item in resultlist:
                fp.writelines(item+'\n')
            fp.flush()
            resultlist = [] #每个规则处理完后要清空这个list
    return filename



def filter(string): #密码约束规则过滤

    specialchar = 1
    number = 2
    upperletter =4
    lowerletter =8
    FLAG = 0

    flag = 0
    kind = 0
    for x in string:
        if 32 <= ord(x) <= 47 or 58<=ord(x)<=64 or 91 <= ord(x) <= 96 or 123 <= ord(x) <=126: #特殊字符
            flag += specialchar
            kind += 1
        if 48 <= ord(x) <= 57: #数字
            flag += number
            kind += 1
        if 65 <= ord(x) <= 90: #大写字母
            flag += upperletter
            kind += 1
        if 97 <= ord(x) <= 122: #小写字母
            flag += lowerletter
            kind += 1

    if config.need_nummber:
        FLAG += number
    if config.need_upper_letter:
        FLAG += upperletter
    if config.need_lower_letter:
        FLAG += lowerletter
    if config.need_special_char:
        FLAG += specialchar

    if len(string)>= config.min_lenth and kind >= config.kinds_needed and  (FLAG & flag == FLAG):
        return True
    else:
        return False

def filter_file(filename):
    logger.info("Doing filter base on the password requirements ...")
    tmplist = []
    fpr = open(filename, "r")  # 写句柄不能用于读
    for item in fpr.readlines():
        if filter(item.strip()):
            tmplist.append()

    fpw = open(filename, "wb")#这里要覆盖写入
    for item in tmplist:
        fpw.write(item)
    fpw.flush()
    fpw.close()

def caps(filename):
    logger.info("Doing capitalize for all passwords have generated ...")
    tmplist = []
    fpr = open(filename, "r")  # 写句柄不能用于读
    # print fpr.readlines()
    for item in fpr.readlines():
        x = item.capitalize()
        if x != item:
            tmplist.append(x)
    fpr.close()
    # print tmplist

    fpw = open(filename, "a")
    for item in tmplist:
        fpw.write(item)
    fpw.flush()
    fpw.close()

def leetit(filename):
    logger.info("Doing leet change for all passwords have generated ...")
    tmplist = []
    fpr = open(filename, "r")
    for item in fpr.readlines():
        for x in item:
            if x in config.leet2num.keys():
                leeted = item.replace(x,dict[x])
                tmplist.append(leeted)

    fpw = open(filename, "a")
    for item in tmplist:
        fpw.write(item)
    fpw.flush()
    fpw.close()


if __name__ == "__main__":
    filename = passmaker()
    if config.capitalize:
        caps(filename)
    if config.leet:
        leetit(filename)
    filter(filename)
    logger.info("Password file: {}".format(os.path.join(os.getcwd(),filename)))
