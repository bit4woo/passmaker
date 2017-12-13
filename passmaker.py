# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import config
import inspect
import itertools
import datetime
import os
from lib.common import logger
import argparse
import argcomplete
import interactive
from argparse import RawTextHelpFormatter


def parse_args():
    print "You can use -i option to use interactive mode"
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description= \
        "Usage: python passmaker.py <OPTIONS> \n")

    menu_group = parser.add_argument_group('Menu Options')

    menu_group.add_argument('-o', '--output', help="password dict file", default=None)
    menu_group.add_argument('-i', '--interactive', help="interactive mode",action='store_true',default=False)
    menu_group.add_argument('-g', '--gui', help="GUI mode", action='store_true', default=True)

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

class passmaker():
    def __init__(self,isinteractive= False,output_file= None):
        self.logger = logger()
        self.output_file = output_file
        if isinteractive:
            config_para = interactive.interactive().interactive()
            for item in config_para:
                setattr(self, item, config_para[item])
        else:
            self.seed_map = {}
            for item in getseedname():  # for step one
                self.seed_map[item] = getseedvalue(item)

            self.rule_list = config.rule_list  # for step two
            self.keep_in_order = config.keep_in_order

            self.leet = config.leet  # for step three
            self.capitalize = config.capitalize

            self.addtional_list = config.addtional_list  # for step 4  list of file

            self.enable_filter = config.enable_filter  # for step 5
            self.min_lenth = config.min_lenth
            self.filter_rule = config.filter_rule
            self.kinds_needed = config.kinds_needed  # 四者包含其三

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
        self.logger.info("making password base one the rule...")
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        if self.output_file:
            filename = self.output_file
        else:
            filename = "passmaker{0}.txt".format(timestr)

        resultlist = []
        templist = []
        rulelist = []
        for item in self.rule_list: #所有规则
            if self.keep_in_order == False:
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
                        if i in self.seed_map: #seed 是否有在config中定义
                            if len(resultlist) == 0:
                                resultlist = self.seed_map[i]
                            else:
                                for x in resultlist:
                                    for y in self.seed_map[i]:
                                        y = y.strip()
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
                self.write_add(filename,resultlist)
                resultlist = [] #每个规则处理完后要清空这个list
        return filename



    def filter(self,string): #密码约束规则过滤

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

        if self.filter_rule["Nummber"]:
            FLAG += number
        if self.filter_rule["Upper_letter"]:
            FLAG += upperletter
        if self.filter_rule["Lower_letter"]:
            FLAG += lowerletter
        if self.filter_rule["Special_char"]:
            FLAG += specialchar

        if len(string)>= self.min_lenth and kind >= self.kinds_needed and  (FLAG & flag == FLAG):
            return True
        else:
            return False

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
                if x in config.leet2num.keys():
                    leeted = item.strip().replace(x,config.leet2num[x])
                    tmplist.append(leeted)
        self.write_add(filename,tmplist)

    def addpassworddict(self,filename): #step five
        self.logger.info("Adding common weak password to result ...")
        tmplist = []
        for item in self.addtional_list:
            if os.path.isfile(item):
                fp = open(item,"r")
                for it in fp.readlines():
                    tmplist.append(it.strip("\n").strip("\r"))
                self.write_add(filename,tmplist)
    def run(self):
        if self.seed_map.keys()>=2 and len(self.rule_list) >=1:
            file = self.passmaker()
            if self.capitalize:
                self.caps(file)
            else:
                self.logger.info("CAPS = False. Skip this step ...")
            if self.leet:
                self.leetit(file)
            else:
                self.logger.info("Leet = False. Skip this step ...")
            self.addpassworddict(file)
            if self.enable_filter:
                self.filter_file(file)
            else:
                self.logger.info("Filter disabled. Skip this step...")
            return file
        else:
            self.logger.info("Config Not complete ... Program Terminated.")
            return None


if __name__ == "__main__":
    args = parse_args()
    pm = passmaker(args.interactive,args.output) #实例化对象
    filename = pm.run()
    if filename:
        logger().info("Password file: {0}".format(os.path.join(os.getcwd(),filename)))
