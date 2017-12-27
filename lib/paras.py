# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.datatype import AttribDict

paras = AttribDict()

paras.seed_map = {}
paras.seed_map["year"] = ["2016","2017","2018"]
paras.seed_map["domain"] = ["baidu.com","badidu","Baidu.com","bd"]
paras.seed_map["specialchar"] = ["!","@","#","$","%","^","&","*","(",")",]

paras.rule_list = []
paras.rule_list.append("domain+year")
paras.keep_in_order = True

paras.leet = False
paras.capitalize = False
'''
paras.leet2num={"a":"4",
                "i":"1",
                "e":"3",
                "t":"7",
                "o":"0",
                "s":"5",
                "g":"9",
                "z":"2"}
paras.leet2string ={
                "O" : "()",
                "U" : "|_|",
                "D" : "|)",
                "W" : "\/\/",
                "S" : "$",
                }
'''
paras.leet_rule={"a":"@"}

paras.additional_list = []

paras.enable_filter = False
paras.min_lenth = 6
paras.filter_rule = {"Upper_letter": False, "Lower_letter": True, "Special_char": False, "Nummber": False}
paras.kinds_needed = 1


if __name__ == "__main__":
    paras = AttribDict()
    #paras = dict()
    paras.path = "xxx"
    paras.xxx = {"a":1,"b":2}
    paras.path = "yyy"
    print paras
