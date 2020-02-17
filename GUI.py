# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4woo'
__github__ = 'https://github.com/bit4woo'

from Tkinter import *
from lib.common import logger,strip_list
from lib.paras import paras
import tkFileDialog
import passmaker
import os

class GUI():
    def __init__(self):
        self.logger = logger()
        self.step = 1
        self.result=[]
        self.createWidgets()

    def step1frame(self,root):
        #######################step one frame########################################
        step1frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        #step1frame.pack()

        label_seed_name = Label(step1frame, text="Step one(Define seeds that use to combine to password):",width=120)
        label_seed_name.grid(row=0, column=0,columnspan=7)

        seed_name = StringVar()
        seed_name_input = Entry(step1frame, textvariable=seed_name, width=20)
        seed_name.set("")
        seed_name_input.focus()
        seed_name_input.grid(row=1, column=0)

        seed_value = StringVar()
        seed_value_input = Entry(step1frame, textvariable=seed_value, width=100)
        seed_value.set("")
        seed_value_input.grid(row=1, column=1, columnspan=5)

        listb = Listbox(step1frame)
        listb.grid(row=2, column=0, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def show_seeds():
            listb.delete(0, END)
            for item in paras.seed_map.keys():
                listb.insert(0, "{0} : {1}".format(item,paras.seed_map[item]))

        def addseed():
            key = seed_name_input.get()
            value = seed_value_input.get()
            value_list = value.split(",")
            if key != "" and value != "":
                paras.seed_map[key] = value_list
                show_seeds()
                self.logger.info("seed {0} : {1}added".format(key,value_list))

        def delseed():
            try:
                x = listb.selection_get()
                key = x.split(":")[0].strip()
                value = x.split(":")[1]
                paras.seed_map.pop(key)
                show_seeds()
                self.logger.info("seed {0} deleted".format(key))
            except Exception, e:
                self.logger.error(e)

        def editseed():
            try:
                x = listb.selection_get()
                key = x.split(":")[0].strip()
                value = paras.seed_map[key]
                seed_name.set(key)
                seed_value.set(",".join(value))
                paras.seed_map.pop(key)
                show_seeds()
                self.logger.info("Editing seed {0} ".format(key))
            except Exception, e:
                self.logger.error(e)

        def chosefile():
            filename = tkFileDialog.askopenfilename(filetypes=[('txt', '*.txt')])
            try:
                tmplist = open(filename, "r").readlines()
                tmplist = strip_list(tmplist)
                seed_value.set(",".join(tmplist))
            except:
                print('Could not open File:%s' % filename)

        def showhelp():
            pass

        button_chosefile = Button(step1frame, text="Chose File", command=chosefile, width=10).grid(row=1, column=7)
        button_add = Button(step1frame, text="Add", command=addseed, width=10).grid(row=2, column=7)
        button_del = Button(step1frame, text="Delete", command=delseed, width=10).grid(row=3, column=7)
        button_edit = Button(step1frame, text="Edit", command=editseed, width=10).grid(row=4, column=7)
        button_help = Button(step1frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)
        #button_pre = Button(step1frame, text="Previous", command=editseed, width =10).grid(row=22, column=2)
        #button_edit = Button(step1frame, text="Next", command=nextstep, width =10).grid(row=22, column=4)
        show_seeds()
        return step1frame

    def step2frame(self,root):
        #######################step two frame########################################
        step2frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        #step2frame.pack()

        label_seed_name = Label(step2frame, text="Step Two(Define rules that how to combine seeds):",width=120)
        label_seed_name.grid(row=0, column=0, columnspan=7)

        def updatePara():
            paras.keep_in_order = isKeepOrder.get()
            #print paras

        isKeepOrder = BooleanVar()
        isKeepOrder.set(paras.keep_in_order)
        keepInOrder = Checkbutton(step2frame, text="Keep same order withe rule when combine", variable=isKeepOrder,command= updatePara)
        keepInOrder.grid(row=1, column=0)


        rule = StringVar()
        rule_input = Entry(step2frame, textvariable=rule, width=20 * 6)
        rule.set("rule")
        rule_input.focus()
        rule_input.grid(row=2, column=0, columnspan =3)

        listb = Listbox(step2frame)
        listb.grid(row=3, column=0, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def check_rule(rule):
            for x in rule.split("+"):
                if x.strip() not in paras.seed_map.keys():
                    print "{0} is not in seeds,Please check".format(x.strip())
                    return False
            return True

        def show_rule():
            listb.delete(0, END)
            for item in list(set(paras.rule_list)):
                listb.insert(0, item)

        def addrule():
            rule = rule_input.get()
            if (rule != "") and (rule not in paras.rule_list) and check_rule(rule):
                paras.rule_list.append(rule)
                show_rule()
                self.logger.info("rule {0} added".format(rule))

        def delrule():
            try:
                x = listb.selection_get()
                paras.rule_list.remove(x)
                show_rule()
                self.logger.info("rule {0} deleted".format(x))
            except Exception, e:
                self.logger.error(e)

        def editrule():
            try:
                x = listb.selection_get()
                paras.rule_list.remove(x)
                show_rule()
                self.logger.info("Editing rule {0} ".format(x))
            except Exception, e:
                self.logger.error(e)

        button_add = Button(step2frame, text="Add", command=addrule, width=10).grid(row=2, column=7)
        button_del = Button(step2frame, text="Delete", command=delrule, width=10).grid(row=3, column=7)
        button_edit = Button(step2frame, text="Edit", command=editrule, width=10).grid(row=4, column=7)
        #button_help = Button(step2frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)
        show_rule()
        return step2frame

    def step3frame(self,root):
        #######################step three frame########################################
        step3frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        #step3frame.pack()

        label_seed_name = Label(step3frame, text="Step Three(Set leet and caps config):",width=120)
        label_seed_name.grid(row=0, column=0,columnspan=7)

        def updatePara():
            paras.capitalize = isEnabledCaps.get()
            #print paras
        isEnabledCaps = BooleanVar()
        isEnabledCaps.set(paras.capitalize)
        EnableCaps = Checkbutton(step3frame, text="Enable Caps First Letter", variable=isEnabledCaps, command= updatePara)
        EnableCaps.grid(row=1, column=0)

        def Leet():
            paras.leet = isEnabledLeet.get()
            if isEnabledLeet.get():
                button_chosefile['state'] = 'normal'
                button_add['state'] = 'normal'
                button_del['state'] = 'normal'
                button_edit['state'] = 'normal'
            else:
                button_chosefile['state'] = 'disabled'
                button_add['state'] = 'disabled'
                button_del['state'] = 'disabled'
                button_edit['state'] = 'disabled'

        isEnabledLeet = BooleanVar()
        isEnabledLeet.set(paras.leet)
        EnableLeet = Checkbutton(step3frame, text="Enable Leet", variable=isEnabledLeet,command=Leet )
        EnableLeet.grid(row=1, column=1)


        leet_rule = StringVar()
        leet_rule_input = Entry(step3frame, textvariable=leet_rule, width=20 * 6)
        leet_rule.set("")
        leet_rule_input.focus()
        leet_rule_input.grid(row=2, column=0, columnspan =3)

        listb = Listbox(step3frame)
        listb.grid(row=3, column=0, columnspan=3, rowspan=20, sticky=W + E + N + S)

        def show_leet_rule():
            listb.delete(0, END)
            for item in paras.leet_rule.keys():
                listb.insert(0, item + ":" + paras.leet_rule[item])

        def addLeetRule():
            key = leet_rule_input.get().split(":")[0].strip()
            value = leet_rule_input.get().split(":")[1].strip()
            if key != "" and value != "" and " " not in leet_rule_input.get():
                paras.leet_rule[key] = value
                show_leet_rule()
                self.logger.info("leet rule {0} added".format(key + ":" + value))

        def delLeetRule():
            try:
                x = listb.selection_get()
                key = x.split(":")[0]
                value = x.split(":")[1]
                paras.leet_rule.pop(key)
                show_leet_rule()
                self.logger.info("leet rule {0} deleted".format(x))
            except Exception, e:
                self.logger.error(e)

        def editLeetRule():
            try:
                x = listb.selection_get()
                key = x.split(":")[0]
                leet_rule.set(x)
                paras.leet_rule.pop(key)
                show_leet_rule()
                self.logger.info("Editing leet rule {0} ".format(x))
            except Exception, e:
                self.logger.error(e)

        def chosefile():
            filename = tkFileDialog.askopenfilename(filetypes=[('txt', '*.txt')])
            try:
                tmplist = open(filename, "r").readlines()
                tmplist = strip_list(tmplist)
                for item in tmplist:
                    key = item.split(":")[0]
                    value = item.split(":")[1]
                    paras.leet_rule[key]= value
                show_leet_rule()
            except Exception,e:
                self.logger('Error: {0} occurs when loading {1}'.format(e,filename))

        button_chosefile = Button(step3frame, text="Load file", command=chosefile, width=10)
        button_chosefile.grid(row=2, column=7)
        button_add = Button(step3frame, text="Add", command=addLeetRule, width=10)
        button_add.grid(row=3, column=7)
        button_del = Button(step3frame, text="Delete", command=delLeetRule, width=10)
        button_del.grid(row=4, column=7)
        button_edit = Button(step3frame, text="Edit", command=editLeetRule, width=10)
        button_edit.grid(row=5, column=7)
        Leet() #设置button的最初状态
        #button_help = Button(step3frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)
        show_leet_rule()
        return step3frame

    def step4frame(self,root):
        #######################step three frame########################################
        step4frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        #step3frame.pack()

        label_seed_name = Label(step4frame, text="Step Four(Add Additional password file):",width=120)
        label_seed_name.grid(row=0, column=0,columnspan =7)

        leet_rule = StringVar()
        leet_rule_input = Entry(step4frame, textvariable=leet_rule, width=20 * 6)
        leet_rule.set("")
        leet_rule_input.focus()
        leet_rule_input.grid(row=1, column=0, columnspan =3)

        listb = Listbox(step4frame)
        listb.grid(row=2, column=0, columnspan=3, rowspan=20, sticky=W + E + N + S)

        def show_additional_file():
            listb.delete(0, END)
            for item in paras.additional_list:
                listb.insert(0, item)

        def delfile():
            try:
                x = listb.selection_get()
                paras.additional_list.remove(x)
                show_additional_file()
                self.logger.info("leet rule {0} deleted".format(x))
            except Exception, e:
                self.logger.error(e)

        def chosefile():
            filename = tkFileDialog.askopenfilename(filetypes=[('txt', '*.txt')])
            try:
                if filename not in paras.additional_list:
                    paras.additional_list.append(filename)
                    leet_rule.set(filename)
                    show_additional_file()
                    self.logger.info('Additional password file {0} added'.format(filename))
            except Exception,e:
                self.logger.info('Error: {0} occurs when loading {1}'.format(e,filename))

        button_chosefile = Button(step4frame, text="Load file", command=chosefile, width=10).grid(row=1, column=7)
        #button_add = Button(step3frame, text="Add", command=addLeetRule, width=10).grid(row=2, column=7)
        button_del = Button(step4frame, text="Delete", command=delfile, width=10).grid(row=3, column=7)
        #button_help = Button(step3frame, text="Help", command=showhelp, width=10).grid(row=6, column=7)
        show_additional_file()
        return step4frame

    def step5frame(self,root):
        #######################step three frame########################################
        step5frame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)

        label_seed_name = Label(step5frame, text="Step Five(Define filter rule and Run Generation):",width=120)
        label_seed_name.grid(row=0, column=0,columnspan=7)

        def setFilter():
            paras.enable_filter = enable_filter.get()
            if paras.enable_filter:
                Upper["state"] = "normal"
                Lower['state'] = 'normal'
                Special['state'] = 'normal'
                Num['state'] = 'normal'
                length_input['state'] = 'normal'
                kinds_input['state'] = 'normal'
            else:
                Upper["state"] = "disabled"
                Lower['state'] = 'disabled'
                Special['state'] = 'disabled'
                Num['state'] = 'disabled'
                length_input['state'] = 'disabled'
                kinds_input['state'] = 'disabled'

            #paras.filter_rule.Upper_letter = Upper_letter.get()
            #print paras
        enable_filter = BooleanVar()
        filter= Checkbutton(step5frame, text="Enable Filter", variable=enable_filter,command = setFilter)
        enable_filter.set(paras.enable_filter)
        filter.grid(row=1, column=0)

        def setUpper():
            paras.filter_rule["Upper_letter"] = Upper_letter.get()
            #paras.filter_rule.Upper_letter = Upper_letter.get()
            #print paras
        Upper_letter = BooleanVar()
        Upper= Checkbutton(step5frame, text="Need Upper Letter in password", variable=Upper_letter,command = setUpper)
        Upper_letter.set(paras.filter_rule["Upper_letter"])
        Upper.grid(row=2, column=0)

        def setLower():
            paras.filter_rule["Lower_letter"] = Lower_letter.get()
        Lower_letter = BooleanVar()
        Lower= Checkbutton(step5frame, text="Need Lower Letter in password", variable=Lower_letter,command = setLower)
        Lower_letter.set(paras.filter_rule["Lower_letter"])
        Lower.grid(row=2, column=1)

        def setSpecial():
            paras.filter_rule["Special_char"] = Special_char.get()
        Special_char = BooleanVar()
        Special= Checkbutton(step5frame, text="Need Special Char in password", variable=Special_char,command = setSpecial)
        Special_char.set(paras.filter_rule["Special_char"])
        Special.grid(row=3, column=0)

        def setNumber():
            paras.filter_rule["Nummber"] = Nummber.get()
        Nummber = BooleanVar()
        Num= Checkbutton(step5frame, text="Need Number in password", variable=Nummber,command = setNumber)
        Nummber.set(paras.filter_rule["Nummber"])
        Num.grid(row=3, column=1)

        lengthLabel = Label(step5frame, text="Min Length of password")
        lengthLabel.grid(row=4, column=0)

        length = IntVar()
        length_input = Entry(step5frame, textvariable=length, width=20)
        length.set(paras.min_lenth)
        length_input.grid(row=4, column=1)

        kindsLabel = Label(step5frame, text="How Many Kinds Needed (Upper Letter、Lower Letter、Special Char、Number)")
        kindsLabel.grid(row=5, column=0)

        kinds = IntVar()
        kinds_input = Entry(step5frame, textvariable=kinds, width=20)
        kinds.set(paras.kinds_needed)
        #kinds_input.focus()
        kinds_input.grid(row=5, column=1)

        listb = Listbox(step5frame)
        listb.grid(row=6, column=0, columnspan=6, rowspan=20, sticky=W + E + N + S)

        def show_password(filename):
            listb.delete(0, END)
            self.result = open(filename,"r").readlines()
            for item in self.result:
                listb.insert(0, item)

        def savetofile():
            name = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
            try:
                name.writelines(self.result)
            except:
                print('Could not open File:%s' % name)

        def Generate():
            paras.kinds_needed = kinds.get()
            paras.min_lenth = length.get()
            print paras
            filename = passmaker.passmaker().run()
            if filename:
                show_password(filename)
                logger().info("Password file: {0}".format(os.path.join(os.getcwd(), filename)))
        def copy():
            import win32clipboard as w
            import win32con
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_TEXT, "".join(self.result))
            w.CloseClipboard()
        button_add = Button(step5frame, text="Generate", command=Generate, width=10).grid(row=6, column=7)
        button_del = Button(step5frame, text="Copy", command=copy, width=10).grid(row=7, column=7)
        button_edit = Button(step5frame, text="Save as", command=savetofile, width=10).grid(row=8, column=7)
        setFilter()#创建完成初始化设置个组件状态
        return step5frame

    def controlFrame(self,root):
        def nextstep():
            if self.step<=4:
                self.step += 1
                self.logger.info("Step {0}:".format(self.step))
            self.showStepFrame(root)

        def pristep():
            if self.step >= 2:
                self.step -= 1
                self.logger.info("Step {0}:".format(self.step))
            self.showStepFrame(root)

        controlFrame = Frame(root)
        button_pre = Button(controlFrame, text="Previous", command=pristep, width=10).grid(row=22, column=2)
        button_edit = Button(controlFrame, text="Next", command=nextstep, width=10).grid(row=22, column=4)
        return controlFrame

    def showStepFrame(self,root):
        if self.step == 1:
            for item in root.winfo_children():
                item.destroy()
            frame = Frame(root)
            self.step1frame(frame).pack()
            self.controlFrame(frame).pack()
            frame.grid(sticky=W + E + N + S)
        if self.step == 2:
            for item in root.winfo_children():
                item.destroy()
            frame = Frame(root)
            self.step2frame(frame).pack()
            self.controlFrame(frame).pack()
            frame.grid(sticky=W + E + N + S)

        if self.step == 3:
            for item in root.winfo_children():
                item.destroy()
            frame = Frame(root)
            self.step3frame(frame).pack()
            self.controlFrame(frame).pack()
            frame.grid(sticky=W + E + N + S)
        if self.step == 4:
            for item in root.winfo_children():
                item.destroy()
            frame = Frame(root)
            self.step4frame(frame).pack()
            self.controlFrame(frame).pack()
            frame.grid(sticky=W + E + N + S)
        if self.step == 5:
            for item in root.winfo_children():
                item.destroy()
            frame = Frame(root)
            self.step5frame(frame).pack()
            self.controlFrame(frame).pack()
            frame.grid(sticky=W + E + N + S)

    def createWidgets(self):
        root = Tk()                     # 创建窗口对象的背景色
        root.title("passmaker by bit4woo")    # 设置窗口标题
        root.geometry()    # 设置窗口大小 注意：是x 不是*
        root.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
        self.showStepFrame(root)
        root.mainloop()                 # 进入消息循环

if __name__ == "__main__":
    GUI()
    print paras