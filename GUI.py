# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from Tkinter import *
from lib.common import logger,strip_list
from tkinter import filedialog

class GUI():
    def __init__(self):
        self.seed_map = {}  # for step one ,dict

        self.rule_list = []  # for step two
        self.keep_in_order = True

        self.leet = False  # for step three
        self.capitalize = False

        self.addtional_list = []  # for step 4  list of file

        self.enable_filter = False  # for step 5
        self.min_lenth = 8
        self.filter_rule = {"Upper_letter": False, "Lower_letter": True, "Special_char": False, "Nummber": False}
        self.kinds_needed = 3  # 四者包含其三

        self.logger = logger()
        self.createWidgets()


    def step1frame(self,root):
        #######################step one frame########################################
        step1frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        step1frame.pack()

        label_seed_name = Label(step1frame, text="Step one(add seeds):")
        label_seed_name.grid(row=0, column=1)

        seed_name = StringVar()
        seed_name_input = Entry(step1frame, textvariable=seed_name, width=20)
        seed_name.set("name")
        seed_name_input.focus()
        seed_name_input.grid(row=1, column=1)

        seed_value = StringVar()
        seed_value_input = Entry(step1frame, textvariable=seed_value, width=100)
        seed_value.set("value")
        seed_value_input.grid(row=1, column=2, columnspan=5)

        listb = Listbox(step1frame)
        listb.grid(row=2, column=1, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def addseed():
            key = seed_name_input.get()
            value = seed_value_input.get()
            if key != "" and value != "":
                self.seed_map[key] = value
                show_seeds()
                self.logger.info("seed {0} added".format(key + " : " + value))

        def delseed():
            try:
                x = listb.selection_get()
                key = x.split(" : ")[0]
                value = x.split(" : ")[1]
                self.seed_map.pop(key)
                show_seeds()
                self.logger.info("seed {0} deleted".format(key + " : " + value))
            except Exception, e:
                self.logger.error(e)

        def editseed():
            try:
                x = listb.selection_get()
                key = x.split(" : ")[0]
                value = x.split(" : ")[1]
                seed_name.set(key)
                seed_value.set(value)
                self.seed_map.pop(key)
                show_seeds()
                self.logger.info("Editing seed {0} ".format(key + " : " + value))
            except Exception, e:
                self.logger.error(e)

        def chosefile():
            filename = filedialog.askopenfilename(filetypes=[('txt', '*.*')])
            try:
                tmplist = open(filename, "r").readlines()
                tmplist = strip_list(tmplist)
                seed_value.set(filename)
            except:
                print('Could not open File:%s' % filename)

        def showhelp():
            pass

        button_chosefile = Button(step1frame, text="Chose File", command=chosefile, width=10).grid(row=1, column=7)
        button_add = Button(step1frame, text="Add", command=addseed, width=10).grid(row=2, column=7)
        button_del = Button(step1frame, text="Delete", command=delseed, width=10).grid(row=3, column=7)
        button_edit = Button(step1frame, text="Edit", command=editseed, width=10).grid(row=4, column=7)
        button_help = Button(step1frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)

        # button_pre = Button(step1frame, text="Previous", command=editseed, width =10).grid(row=22, column=2)
        # button_edit = Button(step1frame, text="Next", command=editseed, width =10).grid(row=22, column=4)


        def show_seeds():
            listb.delete(0, END)
            for item in self.seed_map.keys():  # 第一个小部件插入数据
                listb.insert(0, item + " : " + self.seed_map[item])

    def step2frame(self,root):
        #######################step two frame########################################
        step2frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        step2frame.pack()

        label_seed_name = Label(step2frame, text="Step Two(define rules):")
        label_seed_name.grid(row=0, column=1)

        rule = StringVar()
        rule_input = Entry(step2frame, textvariable=rule, width=20 * 6)
        rule.set("rule")
        rule_input.focus()
        rule_input.grid(row=1, column=1)

        listb = Listbox(step2frame)
        listb.grid(row=2, column=1, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def show_rule():
            listb.delete(0, END)
            for item in list(set(self.rule_list)):
                listb.insert(0, item)

        def addrule():
            rule = rule_input.get()
            if rule != "":
                self.rule_list.append(rule)
                show_rule()
                self.logger.info("rule {0} added".format(rule))

        def delrule():
            try:
                x = listb.selection_get()
                self.rule_list.pop(x)
                show_rule()
                self.logger.info("rule {0} deleted".format(x))
            except Exception, e:
                self.logger.error(e)

        def editrule():
            try:
                x = listb.selection_get()
                self.rule_list.pop(x)
                show_rule()
                self.logger.info("Editing rule {0} ".format(x))
            except Exception, e:
                self.logger.error(e)

        button_add = Button(step2frame, text="Add", command=addrule, width=10).grid(row=2, column=7)
        button_del = Button(step2frame, text="Delete", command=delrule, width=10).grid(row=3, column=7)
        button_edit = Button(step2frame, text="Edit", command=editrule, width=10).grid(row=4, column=7)
        #button_help = Button(step2frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)

    def step3frame(self,root):
        #######################step three frame########################################
        step3frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        step3frame.pack()

        label_seed_name = Label(step3frame, text="Step Three(leet and caps config):")
        label_seed_name.grid(row=0, column=1)

        isEnabledCaps = IntVar()
        EnableCaps = Checkbutton(step3frame, text="Enable Caps and Leet", variable=isEnabledCaps)
        # EnableCaps.grid(row=0, column=2)

        rule = StringVar()
        rule_input = Entry(step3frame, textvariable=rule, width=20 * 6)
        rule.set("rule")
        rule_input.focus()
        rule_input.grid(row=1, column=1)

        listb = Listbox(step3frame)
        listb.grid(row=2, column=1, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def show_leet():
            listb.delete(0, END)
            for item in list(set(self.rule_list)):
                listb.insert(0, item)

        def addrule():
            rule = rule_input.get()
            if rule != "":
                self.rule_list.append(rule)
                show_rule()
                self.logger.info("rule {0} added".format(rule))

        def delrule():
            try:
                x = listb.selection_get()
                self.rule_list.pop(x)
                show_rule()
                self.logger.info("rule {0} deleted".format(x))
            except Exception, e:
                self.logger.error(e)

        def editrule():
            try:
                x = listb.selection_get()
                self.rule_list.pop(x)
                show_rule()
                self.logger.info("Editing rule {0} ".format(x))
            except Exception, e:
                self.logger.error(e)

        button_add = Button(step3frame, text="Add", command=addrule, width=10).grid(row=2, column=7)
        button_del = Button(step3frame, text="Delete", command=delrule, width=10).grid(row=3, column=7)
        button_edit = Button(step3frame, text="Edit", command=editrule, width=10).grid(row=4, column=7)
        #button_help = Button(step3frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)
    def createWidgets(self):
        root = Tk()                     # 创建窗口对象的背景色
        root.title("passmaker by bit4")    # 设置窗口标题
        root.geometry()    # 设置窗口大小 注意：是x 不是*
        root.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
        self.step1frame(root)
        self.step2frame(root)
        self.step3frame(root)

        root.mainloop()                 # 进入消息循环

if __name__ == "__main__":
    GUI()