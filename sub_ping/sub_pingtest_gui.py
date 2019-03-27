#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = {'name' : 'liufengqiang',
                'Email' : '395122482@qq.com',
                'Created' : '2019-03-27'}


from tkinter import *
from tkinter import  ttk
from sub_pingtest_data import *
import tkinter.messagebox as tmb

class PingTestGui:
    '''
    界面设计
    '''
    def __init__(self):
        self.win=Tk()
        self.win.geometry('630x290')
        self.win.title('网段测试')
        
        self.labelframe_ip=LabelFrame(self.win,text='请输入起始IP地址')
        self.labelframe_ip.pack(side=TOP,fill=X)

        self.labelfont=('times',10)

        self.text_set=['开始IP','结束IP']
        self.ip_set=['192.168.0.0','192.168.0.255']
        
        self.ip_var=[]
        for i in range(2):
            self.iplabel=Label(self.labelframe_ip,text=self.text_set[i])
            self.iplabel.pack(side=LEFT,anchor=CENTER)
            self.iplabel.config(font=self.labelfont)
    
            self.ipent=Entry(self.labelframe_ip)
            self.ipent.pack(side=LEFT)
            self.ipent.focus()
            self.var=StringVar()
            self.ipent.config(textvariable=self.var)
            self.var.set(self.ip_set[i])
            self.ip_var.append(self.var)

        self.labelframe_show=LabelFrame(self.win,text='扫描结果')
        self.labelframe_show.pack(side=TOP,fill=X)

        self.sheet_title=['IP地址','是否在线','MAC地址','主机名','域名']
        self.columns_set=('a','b','c','d','e')

        self.scrollbar_show=Scrollbar(self.labelframe_show)
        self.scrollbar_show.pack(side=RIGHT,fill=Y)
        self.treeview_show=ttk.Treeview(self.labelframe_show,height=10,show='headings',columns=self.columns_set)

        for i in range(5):
            self.treeview_show.column(self.columns_set[i], width=120, anchor="center")
            self.treeview_show.heading(self.columns_set[i],text=self.sheet_title[i])

        self.scrollbar_show.config(command=self.treeview_show.yview)
        self.treeview_show.config(yscrollcommand=self.scrollbar_show.set)
        self.treeview_show.pack(side=LEFT,fill=BOTH) 
        

        self.startButton=Button(self.labelframe_ip, text='开始扫描',command=self.get_iplist)
        self.startButton.pack(side=LEFT,padx=10)
        self.startButton.config(font=self.labelfont)
        self.win.mainloop()

            
    def get_iplist(self):
        '''
        按扭执行程序，调用sub_pingtest_data.py模块中的类，进行计算
        '''
       
        ip=[]
        checklist=[]
        for ent_ip in self.ip_var:
            ip.append(ent_ip.get())
            chkip=checkip(ent_ip.get())
            checklist.append(chkip.check())
        
        if checklist[0] and checklist[1]:
            ip_list=ipsplit(ip[0],ip[1]).iplist()
        else:
            r6=tmb.showerror('错误','输入IP地址错误，请重新输入')
        
        myque=QueueThreads()
        myque.makethreads(50,ip_list)
        treelist=sorted(myque.returnlist())
        
        self.inserttree(treelist)

    def inserttree(self,treelist):

        for _ in map(self.treeview_show.delete,self.treeview_show.get_children("")):
            pass
        for showlist in treelist:
            self.treeview_show.insert('','end',values=(showlist[0],showlist[1],showlist[2],showlist[3],showlist[4]))
            
       
if __name__ == '__main__':
    
     PingTestGui()
     
