# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4woo'
__github__ = 'https://github.com/bit4woo'

import config
import inspect
import itertools
import datetime
import os
import argparse
import argcomplete
import interactive
import GUI
from argparse import RawTextHelpFormatter
from lib.paras import paras
from lib.common import logger
from lib import common

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description= \
        "Usage: python passmaker.py <OPTIONS> \n")

    menu_group = parser.add_argument_group('Menu Options')

    menu_group.add_argument('-o', '--output', help="password dict file", default=None)
    menu_group.add_argument('-i', '--interactive', help="interactive mode",action='store_true',default=False)
    menu_group.add_argument('-g', '--gui', help="GUI mode", action='store_true', default=False)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    return args

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
        if name == item[0] and isinstance(item[1],list):
            tmplist = []
            for x in item[1]:
                x= x.strip("\r")
                x = x.strip("\n")
                tmplist.append(x)
            return tmplist

def config2Paras():
    paras.seed_map = {}
    for item in getseedname():  # for step one
        paras.seed_map[item] = getseedvalue(item)

    paras.rule_list = config.rule_list  # for step two
    paras.keep_in_order = config.keep_in_order

    paras.leet = config.leet  # for step three
    paras.capitalize = config.capitalize

    paras.additional_list = config.additional_list  # for step 4  list of file

    paras.enable_filter = config.enable_filter  # for step 5
    paras.min_lenth = config.min_lenth
    paras.filter_rule = config.filter_rule
    paras.kinds_needed = config.kinds_needed  # 四者包含其三

class passmaker():
    def __init__(self,isinteractive= False,isGUI = True, output_file= None):
        self.logger = logger()
        self.output_file = output_file

    def write_add(self,filename,write_list):
        try:
            fp = open(filename,"ab+")
            if len(fp.readlines()) !=0:
                fp.write("\n")
            fp.writelines("\n".join(write_list))
            fp.close()
            return 0
        except Exception,e:
            self.logger.error(e)
            return 1

    def passmaker(self): # first step and two ,combine base on the rules.
        self.logger.info("making password base on the rule...")
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        if self.output_file:
            filename = self.output_file
        else:
            filename = os.path.join("output","passmaker{0}.txt".format(timestr))

        resultlist = []
        templist = []
        rulelist = []
        for item in paras.rule_list: #所有规则
            if paras.keep_in_order == False:
                x = item.split("+")
                y = len(x)
                z = itertools.permutations(x, y)#结构是list,
                rulelist = list(set(z))#一个规则变成了多个
                #print rulelist
            else:
                rulelist.append(tuple(item.split("+")))
                #print rulelist

        for item in rulelist: #item 是一个规则,类型是元组
            #print item
            try:
                for i in item: #解析一个规则，i是seed,单个组成部分
                    if i in paras.seed_map: #seed 是否有在config中定义
                        if len(resultlist) == 0:
                            resultlist = paras.seed_map[i]
                        else:
                            for x in resultlist:
                                for y in paras.seed_map[i]:
                                    y = y.strip()
                                    templist.append(x+y)
                            #print resultlist
                            resultlist = templist
                            templist = []
                    else:
                        raise Exception("No \"{0}\" found, Please check your config!".format(i))

            except Exception,e:
                print e
                exit(0)
            #begin write file
            self.write_add(filename,resultlist)
            resultlist = [] #每个规则处理完后要清空这个list
        return filename

    def filter(self,string): #密码约束规则过滤

        #第一重过滤
        if len(string) < paras.min_lenth:#先要满足长度要求，提高过滤速度。
            return False

        hasSpecialchar = False
        hasNumber = False
        hasUpperletter =False
        hasLowerletter =False
        kind = 0

        if common.hasSpecialchar(string):#特殊字符
                hasSpecialchar = True
                kind += 1
        if common.hasNumber(string):#数字
                hasNumber = True
                kind += 1
        if common.hasUpperletter(string): #大写字母
                hasUpperletter = True
                kind += 1
        if common.hasLowerletter(string): #小写字母
                hasLowerletter = True
                kind += 1

        #第2重过滤，需要满足种类种数
        if kind < paras.kinds_needed:
            return False
        else:
            pass

        # 第3重过滤，需要满足种类
        if paras.filter_rule["Nummber"]:
            if not hasNumber:
                return False
        if paras.filter_rule["Upper_letter"]:
            if not hasUpperletter:
                return False
        if paras.filter_rule["Lower_letter"]:
            if not hasLowerletter:
                return False
        if paras.filter_rule["Special_char"]:
            if not hasSpecialchar:
                return False

        return True

    def filter_file(self,filename): # step four
        self.logger.info("Doing filter base on the password requirements ...")

        tmplist = []
        fpr = open(filename, "r")  # 写句柄不能用于读
        for item in fpr.readlines():
            if self.filter(item.strip()):
                tmplist.append(item.strip())

        tmplist = list(set(tmplist)) #去重

        fpw = open(filename, "wb")#这里要覆盖写入
        fpw.writelines("\n".join(tmplist))
        fpw.close()


    def caps(self,filename): # step three
        self.logger.info("Doing capitalize for all passwords have generated ...")
        tmplist = []
        fpr = open(filename, "r")  # 写句柄不能用于读
        # print fpr.readlines()
        for item in fpr.readlines():
            x = item.strip().capitalize()
            if x != item.strip():
                tmplist.append(x)
        fpr.close()
        # print tmplist
        self.write_add(filename,tmplist)
        #return filename

    def leetit(self,filename): #step three
        self.logger.info("Doing leet change for all passwords have generated ...")
        tmplist = []
        fpr = open(filename, "r")
        for item in fpr.readlines():
            for x in item.strip():
                if x in paras.leet_rule.keys():
                    leeted = item.strip().replace(x,paras.leet_rule[x])
                    tmplist.append(leeted)
        self.write_add(filename,tmplist)

    def addpassworddict(self,filename): #step five
        self.logger.info("Adding common weak password to result ...")
        tmplist = []
        for item in paras.additional_list:
            if os.path.isfile(item):
                fp = open(item,"r")
                for it in fp.readlines():
                    tmplist.append(it.strip("\n").strip("\r"))
                self.write_add(filename,tmplist)
    def run(self):
        if paras.seed_map.keys()>=2 and len(paras.rule_list) >=1:
            file = self.passmaker()
            if paras.capitalize:
                self.caps(file)
            else:
                self.logger.info("CAPS = False. Skip this step ...")
            if paras.leet:
                self.leetit(file)
            else:
                self.logger.info("Leet = False. Skip this step ...")
            self.addpassworddict(file)
            if paras.enable_filter:
                self.filter_file(file)
            else:
                self.logger.info("Filter disabled. Skip this step...")
            return file
        else:
            self.logger.info("Config Not complete ...Please check and run again")
            return None


if __name__ == "__main__":
    args = parse_args()
    if args.interactive:
        interactive.interactive().interactive()
        filename = passmaker().run()
        if filename:
            logger().info("Password file: {0}".format(os.path.join(os.getcwd(), filename)))
    elif args.gui:
        GUI.GUI()
    else:
        config2Paras()
        filename = passmaker().run()
        if filename:
            logger().info("Password file: {0}".format(os.path.join(os.getcwd(),filename)))
