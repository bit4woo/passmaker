# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


#第一步，定义种子（seed），密码的基本组成部分,
domain= ["wolaidai.com","wolaidai","welab","welab.com"]
year = ["2016","2017","2018"]
special_letter = ["!","@","#","$","%",]
xxx = open('./seed/weak_password_top100.txt').readlines()
#domain_capitalize = False #域名首字母大写处理


#第二步，定义密码的组成规则
rule = ["domain+special_letter+year"]
keep_in_order = False #以上的规则，是否保持原顺序，如果为False 将对每个规则中的seed进行排列组合后生产密码。



#第三步，对以上生成的密码再进行一些变形处理
capitalize = True  #是否进行首字母大写处理
leet = False       #是否进行变形处理
leet2num = {"a":"4",
            "i":"1",
            "e":"3",
            "t":"7",
            "o":"0",
            "s":"5",
            "g":"9",
            "z":"2"}

leet2string ={
            "O" : "()",
            "U" : "|_|",
            "D" : "|)",
            "W" : "\/\/",
            "S" : "$",
            }


#第四步，根据以下密码规则约束，对以上生成的密码进行过滤处理，删除不满足条件的
min_lenth =8
need_upper_letter = False
need_lower_letter = True
need_special_char = False
need_nummber = False
#大写字母、小写字母、特殊符号、数字,四种包含三种---常见的密码要求
kinds_needed = 3  #四者包含其三

if __name__ =="__main__":
    print type(xxx)