#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
from MyWindowClass import MyFrame,MyButton,MyLabel,MyEntry
from IPy import IP
win=Tk()
win.title('IP计算')
win.iconbitmap('/nettool/22.ico')
frame1=MyFrame(win)
frame1.pack(side=TOP,expand=YES,fill=BOTH)

labelfont=('times',10)

input_iplabel=MyLabel(frame1,text='请输入IP')
input_iplabel.grid(row=0,column=0,sticky=NSEW)
input_iplabel.config(font=labelfont)

input_ipEnt=MyEntry(frame1)
input_ipEnt.insert(0,'192.168.0.0')
input_ipEnt.grid(row=0,column=1,sticky=NSEW)
input_ipEnt.focus()

input_masklabel=MyLabel(frame1,text='请输入掩码1-32')
input_masklabel.grid(row=1,column=0,sticky=NSEW)
input_masklabel.config(font=labelfont)

input_maskEnt=MyEntry(frame1)
input_maskEnt.insert(0,'24')
input_maskEnt.grid(row=1,column=1,sticky=NSEW)
input_maskEnt.focus()


msg_var=StringVar(frame1)
msg=Message(frame1,textvariable=msg_var,width=300)
msg.config(bg='white',font=labelfont)
msg.grid(columnspan=2)

def checkip(ip):
    pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
    return re.match(pattern,ip) # 检查IP地址是否合法
def checkmask(mask):
    if 0<int(mask)<32:
        return 1
    else:
        return 0

def startcounter():
    msg_var.set('')
    if checkip(input_ipEnt.get()) and checkmask(input_maskEnt.get()):
        iplist=input_ipEnt.get()+'/'+input_maskEnt.get()
        ips=IP(iplist)
        banben='地址版本：' +str(ips.version())+'\n'
        wangduan='网络地址：'+str(ips.net())+'\n'
        mask='子网掩码：'+str(ips.netmask())+'\n'
        ipshuliang='地址数量：'+str(ips.len())+'\n'
        broad='广播地址：'+str(ips.broadcast())+'\n'
        erjinzhi='二进制地址:：'+ips.strBin()+'\n'
        leixiang='地址类型：' +ips.iptype()+'\n'
        show_result=banben+leixiang+wangduan+mask+ipshuliang+broad+erjinzhi
        print(iplist)
        print(input_ipEnt.get(),input_maskEnt.get())
        msg_var.set(show_result)
        

startButton=MyButton(frame1, text='开始计算',command=startcounter)
startButton.grid(columnspan=2)
startButton.config(font=labelfont)


win.mainloop()
