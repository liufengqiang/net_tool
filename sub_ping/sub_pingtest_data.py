#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = {'name' : 'liufengqiang',
                'Email' : '395122482@qq.com',
                'Created' : '2019-03-27'}

import re
import socket
import subprocess
import platform
import sys
import threading
import queue
from queue import Empty
import time
import pickle


class checkip:
    '''
    检查IP地址是否合法
    '''
    
    def __init__(self,ip='10.0.0.1'):
        self.ip=ip
    def check(self):
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        return re.match(pattern,self.ip)



class ipsplit:
    '''
    输入起始和结束IP地址，返回一个IP地址列表
    '''
    
    def __init__(self,begin_ip='10.10.10.0',end_ip='10.10.10.77'):
        self.begin_ip=begin_ip
        self.end_ip=end_ip
        
    def iplist(self):
        ip_begin_list=self.begin_ip.split('.')
        ip_end_list=self.end_ip.split('.')
        if ip_begin_list[0]==ip_end_list[0] and ip_begin_list[1]==ip_end_list[1] and ip_begin_list[2]==ip_end_list[2]:
            iplist=[]
            for i in range(int(ip_begin_list[-1]),int(ip_end_list[-1])+1):
                ip=str(ip_begin_list[0]+'.'+ip_begin_list[1]+'.'+ip_begin_list[2]+'.'+str(i))
                iplist.append(ip)
        return iplist



class getHostbyIP:
    '''
    根据输入的IP地址获得相应的主机名、域和MAC地址
    '''
    def __init__(self,ip='10.10.31.10'):
        self.ip=ip
        
    def gethostmac(self):
        try:
            result=socket.gethostbyaddr(self.ip)
            host_yu_ip=socket.gethostbyname_ex(result[0])
            hostsplit=host_yu_ip[0].split('.')
            hostname=hostsplit[0]
            yuname='.'.join(hostsplit[1:])
            ret=subprocess.Popen('arp -a {0}'.format(self.ip),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out=str(ret.stdout.read())
            mac=out[177:194]
            res=[mac,hostname,yuname]
        except:
            res=['非电脑地址','','']
        return res


class CmdPingIP:
    '''
    ping指定IP，查看是否在线,在线返回True,不在线返回False
    '''

    def __init__(self,ip='10.0.0.1'):
        self.ip=ip
       

    def get_os(self):
        cmd_ping=''
        os=platform.system()
        if os=="Windows":
            return "n"
        else:
            return "c"
        
    def cmd_ping(self):
        cmd_ping=["ping",self.ip,"-{op}".format(op=self.get_os()),"1"]
        cmd=" ".join(cmd_ping)
        ftp_ret = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        ret = ftp_ret.stdout.read()  
        str_ret = ret.decode("gbk")  
        ret_s = re.search("TTL",str_ret)
        if ret_s:
            return True
        else:
            return False


listshow=[] 
class QueueThreads:
    '''
    一个生产者、消费者的队列线程类，其中消费者可改写
    '''
    
  
    #消费者
    def consumer(self,q):
        global listshow

        singlelistshow=[]

        try:
            while True:
                ip=q.get_nowait()
                yy=CmdPingIP(ip)
                tt=yy.cmd_ping()
                if tt:
                    singlelistshow=getHostbyIP(ip).gethostmac()
                    singlelistshow.insert(0,ip)
                    singlelistshow.insert(1,'在线')
                    listshow.append(singlelistshow)
                q.task_done()
        except Empty:
            pass
            
    #多线程，线程数自定
    def makethreads(self,threads_num,iplist):
        q=queue.Queue()
        for ip in iplist:
            q.put(ip)

        threads=[]
        for i in range(threads_num):
            thr=threading.Thread(target=self.consumer,args=(q,))
            thr.start()
            threads.append(thr)
            
        for thr in threads:
            thr.join()
    def returnlist(self):
        return listshow
    

if __name__=='__main__':
    
          
    ip=['192.168.31.1','50.20.30.4','192.168.31.10','192.16.1.10','192.16.1.11','192.168.31.12','192.168.31.14']

    myque=QueueThreads()

    myque.makethreads(4,ip)
    print (myque.returnlist())
    
    
  
