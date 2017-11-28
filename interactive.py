# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import readline
import glob
import colorama
import os.path

class color:
    def __init__(self):
        colorama.init()
        self.white = colorama.Fore.WHITE
        self.red = colorama.Fore.RED
        self.blue = colorama.Fore.BLUE
        self.green = colorama.Fore.GREEN
        self.yellow = colorama.Fore.YELLOW  # yellow
        self.lightwhite = colorama.Fore.LIGHTWHITE_EX
        self.lightred = colorama.Fore.LIGHTRED_EX
        self.lightblue = colorama.Fore.LIGHTBLUE_EX
        self.lightgreen = colorama.Fore.LIGHTGREEN_EX
        self.lightyellow = colorama.Fore.LIGHTYELLOW_EX
color = color()

class tabCompleter(object):

    def pathCompleter(self,text,state):
        line   = readline.get_line_buffer().split()
        return [x for x in glob.glob(text+'*')][state]



class interactive():
    def __init__(self):
        self.seed_map = {}  # for step one

        self.rule_list = []  # for step two
        self.keep_in_order = True

        self.leet = False  # for step three
        self.capitalize = False

        self.addtional_list = []  # for step 4  list of file

        self.enable_filter = False  # for step 5
        self.min_lenth = 8
        self.filter_rule = {"Upper_letter": False, "Lower_letter": True, "Special_char": False, "Nummber": False}
        self.kinds_needed = 3  # 四者包含其三

    def print_paras(self):
        #print self.__dict__
        print ("\nCurrent config values:\n")
        for a in self.__dict__:
            print ("{0} = {1}".format(a,self.__dict__[a]))

    def interactive(self):
        t = tabCompleter()
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(t.pathCompleter)
        print color.green + "\nWelcome to interactive mode!\n\nNotice: you can input BACK to back to upper menu in each step."
        index = '''
        1.Step one: define the seed
        2.Step two: define the rule that to combine the seed
        3.Step three: whether to leet or caps the result [default both is False]
        4.Step four: add exist list to the result [default is None]
        5.Step five: define the filter to clean result [default Not to filte]
        6.Print current config vulues
        7.Exit/back/run
        '''
        basedir = os.path.dirname(__file__)
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
                    elif "=" in seed_input:
                        key = seed_input.split('=')[0].strip()
                        value = seed_input.split('=')[1].strip()
                        if "file(" in value:
                            file_name = value.replace("file(","").strip(')')
                            try:
                                value_list = open(file_name,"r").readlines()
                            except:
                                file_name = os.path.join(basedir,"seed",file_name)
                                try:
                                    value_list = open(file_name, "r").readlines()
                                except:
                                    print "File Not Found!"
                                    continue
                        else:
                            value_list = value.split(',')
                        self.seed_map[key] = value_list
                    else:
                        continue
            elif step_choice == "2":
                print("Please input your rule,only can use seeds already defined in step one.\n"
                      "Example :\n"
                      "domain+year,domain")
                print("already defined seeds: {0}".format(self.seed_map.keys()))
                def check_rule(rule_list):
                    tmp =[]
                    for item in self.rule_list:
                        for x in item.split("+"):
                            if x.strip() not in self.seed_map.keys():
                                tmp.append(x.strip)
                                print "{0} is not in seeds,Please check".format(x.strip())
                    if len(tmp) == 0:
                        return  True
                    else:
                        print "{0} is not in seeds,Please check and input again".format(tmp)
                        return False
                while True:
                    rule_input = raw_input("==>")
                    if rule_input.lower() == "back":
                        break
                    elif rule_input == "":
                        continue
                    else:
                        self.rule_list = rule_input.split(',')
                        if check_rule(self.rule_list):# true = check pass
                            break
                        else:
                            continue

                while True:
                    order_input = raw_input("whether to keep the seed in order when combine?(Y/n)\n==>")
                    if order_input.lower() == "back":
                        break
                    elif order_input.lower() in ["","y","yes"]:
                        self.keep_in_order = True
                        break
                    elif order_input.lower() in ["no","n"]:
                        self.keep_in_order = False
                        break
                    else:
                        continue


            elif step_choice == "3":
                print("whether to LEET or CAPS the combined result? (None/leet/caps/both)\n")
                while True:
                    leet_input = raw_input("==>")
                    if leet_input.lower() in ["",'none',"n"]:
                        self.capitalize = False
                        self.leet = False
                        break
                    elif leet_input.lower() == 'leet':
                        self.leet = True
                        break
                    elif leet_input.lower() == 'caps':
                        self.capitalize = True
                        break
                    elif leet_input.lower() == 'both':
                        self.capitalize = True
                        self.leet = True
                        break
                    elif leet_input.lower() == 'back':
                        break
                    else:
                        print "Invalid input...."
                        continue

            elif step_choice == "4":
                print("Add addtional common weak passwords to the end of result,input the weak password file\n"
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
                                self.addtional_list.append(file)
                            else:
                                file = os.path.join(basedir,"dict",file.strip())
                                self.addtional_list.append(file)
                        break

            elif step_choice == "5": #filter
                print ("Enable the filter rules to clean result?(Yes/no)\n")
                while True:
                    filter_input = raw_input("==>")
                    if filter_input.lower() in ["no","n"]:
                        self.enable_filter = False
                        break
                    elif filter_input.lower() in ["","y","yes"]:
                        self.enable_filter = True



                        print ("The min length requirement of password\n")
                        while True:
                            filter_options = raw_input("==>")
                            try:
                                self.min_lenth = int(filter_options)
                                break
                            except:
                                continue

                        for item in self.filter_rule.keys():
                            print ("Please chose whether must contains:[{0}] ?({1})\n".format(item,'True/false' if self.filter_rule[item] else 'False/true'))
                            filter_options = raw_input("==>")
                            if filter_options.lower() in ["t","true"]:
                                self.filter_rule[item] = True
                                break
                            elif filter_options.lower() in ["f","false"]:
                                self.filter_rule[item] = False
                                break
                            elif filter_options == "":
                                pass
                            elif filter_options.lower() == "back":
                                break
                            else:
                                continue

                        print ("how many kinds needed of [Upper_letter, Lower_letter, Special_char, Nummber]\n")
                        while True:
                            filter_options = raw_input("==>")
                            try:
                                x = int(filter_options)
                                if 0<= x <= 4:
                                    self.kinds_needed = x
                                    break
                                else:
                                    continue
                            except:
                                continue
                        break
                    elif filter_input.lower() == 'back':
                        break
                    else:
                        continue

            elif step_choice.lower() in ["6","print"]:
                self.print_paras()
            elif step_choice.lower() in ["7","exit","back","run"] :
                break
            else:
                continue
        return self.__dict__

if __name__ == "__main__":
    x = interactive()
    #x.print_paras()
    print x.interactive()
    #x.print_paras()
