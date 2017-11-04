# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import readline
import glob
import colorama
import os.path

class colors:
    colorama.init()
    white = colorama.Fore.WHITE
    red = colorama.Fore.RED
    blue = colorama.Fore.BLUE
    green = colorama.Fore.GREEN


class tabCompleter(object):

    def pathCompleter(self,text,state):
        line   = readline.get_line_buffer().split()
        return [x for x in glob.glob(text+'*')][state]

def interactive():
    t = tabCompleter()
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(t.pathCompleter)
    print colors.white + "\nWelcome to interactive mode!\n\nNotice: you can input BACK to back to upper menu in each step."
    index = '''
    1.Step one: define the seed
    2.Step two: define the rule that to combine the seed
    3.Step three: whether to leet or caps the result[default both is False]
    4.Step four: add exist list to the result[default is None]
    5.Step five: define the filter to clean result
    6.Exit/back
    '''
    seed_map = {}  #for step one
    rule_list = []
    keep_in_order = True
    leet = False
    capitalize = False
    addtional_list =[]

    enable_filter = False
    min_lenth = 1
    filter_rule = { "Upper_letter":False, "Lower_letter":True, "Special_char" : False, "Nummber" : False}
    kinds_needed = 3  # 四者包含其三

    while True:
        step_choice = raw_input(index)
        if step_choice == "1":
            print("Example : \ndomain = baidu.com,BAIDU.com\nyears = file(years.txt)\n")
            while True:
                seed_input = raw_input("==>")
                if seed_input.lower() == "back":
                    break
                elif seed_input == "":
                    continue
                else:
                    key = seed_input.split('=')[0].strip()
                    value = seed_input.split('=')[1].strip()
                    if "file(" in value:
                        file_name = value.replace("file(","").strip(')')
                        value_list = open(file_name,"r").readlines()
                    else:
                        value_list = value.split(',')
                    seed_map[key] = value_list
        elif step_choice == "2":
            print("Please input your rule,only can use seeds already defined in step one.\n"
                  "Example :\n"
                  "domain+year,domain")
            print("already defined seeds: {0}".format(seed_map.keys()))
            while True:
                rule_input = raw_input("==>")
                if rule_input.lower() == "back":
                    break
                elif rule_input == "":
                    continue
                else:
                    rule_list = rule_input.split(',')
            while True:
                order_input = raw_input("whether to keep the seed in order when combine?(Y/n)\n==>")
                if order_input.lower() == "back":
                    break
                elif order_input.lower() in ["","y","yes"]:
                    keep_in_order = True
                elif order_input.lower() in ["no","n"]:
                    keep_in_order = False
                else:
                    continue


        elif step_choice == "3":
            print("whether to LEET or CAPS the combined result? (None/leet/caps/both)\n")
            while True:
                leet_input = raw_input("==>")
                if leet_input.lower() in ["",'none',"n"]:
                    capitalize = False
                    leet = False
                elif leet_input.lower() == 'leet':
                    leet = True
                elif leet_input.lower() == 'caps':
                    capitalize = True
                elif leet_input.lower() == 'both':
                    capitalize = True
                    leet = True
                elif leet_input.lower() == 'back':
                    break
                else:
                    print "Invalid input...."
                    continue

        elif step_choice == "4":
            print("Add addtional common weak passwords to the end of result,input the weak password file\n""
                  "Example: \n"
                  "weak_password_top100.txt,weak_pass_chinese.txt\n")
            while True:
                addtionalitem_input = raw_input("==>")
                if addtionalitem_input.lower() == 'back':
                    break
                elif addtionalitem_input == '':
                    continue
                else:
                    files = addtionalitem_input.strip().split(',')
                    for file in files:
                        if os.path.isfile(file.strip()):
                            addtional_list.extend(open(addtionalitem_input.strip(),'r').readlines())

        elif step_choice == "5": #filter
            print ("Enable the filter rules to clean result?(No/yes)\n")
            while True:
                filter_input = raw_input("==>")
                if filter_input.lower() in ["","no","n"]:
                    enable_filter = False
                elif filter_input.lower() in ["y","yes"]:
                    enable_filter = True


                    print ("The min length requirement of password\n")
                    while True:
                        filter_options = raw_input("==>")
                        try:
                            min_lenth = int(filter_options)
                            break
                        except:
                            continue

                    print ()
                    while True:
                        for item in filter_rule.keys():
                            filter_options = raw_input("Please chose whether must contains:[{0}] ?({1})".format(item,'True/false' if filter_rule[item] else 'False/true'))
                            if filter_options.lower() in ["t","true"]:
                                filter_rule[item] = True
                            elif filter_options.lower() in ["f","false"]:
                                filter_rule[item] = False
                            elif filter_options == "":
                                pass
                            elif filter_options.lower() == "back":
                                break
                            else:
                                continue
                    while True:
                        filter_options = raw_input("how many kinds needed of [Upper_letter, Lower_letter, Special_char, Nummber]")
                        try:
                            x = int(filter_options)
                            if 0<= x <= 4:
                                kinds_needed = x
                            else:
                                continue
                        except:
                            continue

                elif filter_input.lower() == 'back':
                    break
                else:
                    continue

        elif step_choice.lower() in ["6","exit","back"] :
            break
        else:
            continue



if __name__ == "__main__":
    interactive()
