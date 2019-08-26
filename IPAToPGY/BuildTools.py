#-*- coding:utf-8 -*-

import os
import shutil
import getpass
import sys
import tkinter
import tkinter.filedialog
import tkinter.constants
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import plistlib


# 蒲公英相关参数设置
PGY_URL = "http://www.pgyer.com/apiv1/app/upload"
PGY_UKey = "************"
PGY_APIKey = "***************"
PGY_PW = ""
PGY_INSTALL_type = 1

# 开发者网站参数
DeveloperAccountName = "**********"
DeveloperAccountPWD = "**************"

# 邮件的相关参数设置
MAIL_HOST = "smtp.mxhichina.com"
# //邮件标题
MAIL_SUBJECT = "测试版本已经发布"
# //发件人MAIL_
MAIL_FROM = "**************"
Mail_PassWord = "**********"


# // 测试人员邮箱地址
MAILS_TESTER = [
                {"name":"许文杰",
                 "mail":"xuwenjie@ellabook.cn"
                 },
               {
                  'name':'吕陈强',
                   'mail':'lvchenqiang@ellabook.cn'
                },
                {
                  'name':'仇东航',
                  'mail':'qiudonghang@ellabook.cn'
                },
                {
                  'name':'姚明振',
                  'mail':'yaomingzhen@ellabook.cn'
                },
]

# // 用于存放多选按钮的值
MAILS_TESTER_BTN_ARR = []

# // 用于存放选择后的人员邮箱地址
MAILS_TESTER_SELECTER = []


class IPAHelper(object):
    def __init__(self):
        print("初始化打包工具")


    # 设置配置文件路径
    def createFinder(self,path):
        # 没有文件夹，创建文件夹
        if not os.path.exists(path):
            os.system("mkdir %s" % (path))

     # clean工程
    def cleanProject(self,isWorkSpace,filepath,filename):
        if isWorkSpace:
            ok = os.system(
                'cd %s;xcodebuild -workspace %s.xcworkspace -scheme %s clean' % (filepath, filename, filename))
        else:
            ok = os.system('cd %s;xcodebuild -target %s clean' % (filepath, filename))
        return ok

    def buildProject(self,isWorkSpace,filepath,filename,archivePath):

        if not os.path.exists (archivePath):
            os.system ("mkdir %s" % (archivePath))

        if isWorkSpace:
           ok = os.system(
                "cd %s;xcodebuild -workspace %s.xcworkspace -scheme %s -configuration Release  -archivePath %s/%s.xcarchive clean archive" % (
                    filepath, filename, filename, archivePath, filename))
        else:
           ok = os.system(
                "cd %s;xcodebuild -project %s.xcodeproj -scheme %s -configuration Release  -archivePath %s/%s.xcarchive clean archive" % (
                    filepath, filename, filename, archivePath, filename))
        return ok

    def cerateIPA(self,isDev,filepath,filename,archivePath):
        if isDev:
          ok = os.system("cd %s; xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportOptionsPlist %s/DevExportOptions.plist -allowProvisioningUpdates -quiet" % (
              filepath, archivePath, filename, archivePath, filename, os.getcwd()))
        else:
          ok = os.system(
                "cd %s; xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportOptionsPlist %s/DisExportOptions.plist -allowProvisioningUpdates -quiet" % (
                    filepath, archivePath, filename, archivePath, filename, os.getcwd()))
        return ok

    def uploadToPGY(self,archivePath,filename,tagdesc,mailusers):
        if len(mailusers) == 0:
            print("未选择 测试人员信息")
            return
        print ("开始上传到蒲公英")
        path = "%s/%s/%s.ipa" % (archivePath, filename, filename)
        f_op = open (path, 'rb')

        if os.path.exists (path):
            print ("找到ipa文件")
            # 请求参数字典
            params = {
                'uKey': PGY_UKey,
                '_api_key': PGY_APIKey,
                'installType': PGY_INSTALL_type,
                'password': PGY_PW,
                'updateDescription': tagdesc
            }

            response = requests.post (PGY_URL, files={"file": open (path, 'rb')}, data=params)
            print (response.json ())
            if str (response.json ()["code"]) == "0":
               return self.sendMail (response.json ()["data"],mailusers=mailusers)

        else:
            print ("没有找到ipa文件")
        """
          altoolPath="/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"
          ${altoolPath} --validate-app -f ${ipaPath} -u xxxxxx -p xxxxxx -t ios --output-format xml >>
          ${altoolPath} --upload-app -f ${ipaPath} -u xxxxxx -p xxxxxx -t ios --output-format xml

          --validate-app 您要验证指定的 App
          --upload-app   您要上传指定的 App
          -f file        正在验证或上传的 App 的路径和文件名。
          -u username    您的用户名
          -p password    您的用户密码
          --output-format [xml | normal]   您想让 Application Loader 以结构化的 XML 格式还是非结构化的文本格式返回输出信息。默认情况下，Application Loader 以文本格式返回输出信息


          success-message
          product-errors

          """

    def uploadToItunesConnect(self,archivePath,filename):
        ipaPath =  "%s/%s/%s.ipa" % (archivePath, filename, filename)
        print ("上传到ItunesConnect")
        altoolPath = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"
        validateresult = os.popen ("%s --validate-app -f %s/ -u %s -p %s -t ios --output-format xml" % (
        altoolPath, ipaPath, DeveloperAccountName, DeveloperAccountPWD)).read ()
        uploadresult = os.popen ("%s --upload-app -f %s -u %s -p %s -t ios --output-format xml" % (
        altoolPath, ipaPath, DeveloperAccountName, DeveloperAccountPWD)).read ()

        # 处理plist文件
        pl = plistlib.readPlistFromBytes (str (uploadresult).encode ())

        print (pl["product-errors"])
        print ("输出成功")

        fp = open ("1.plist", 'w')
        fp.write (str (uploadresult))
        fp.close ()

        if ("success-message" in str (uploadresult)):
            print ("上传成功")
        elif ("product-errors" in str (uploadresult)):
            print ("上传失败 %s", uploadresult)
        else:
            print ("未知失败原因")
        return
        # self.sendMail ({"appName": targetName,
        #                 "appVersion": "appVersion",
        #                 "appShortcutUrl": "暂无",
        #                 "appUpdated": "暂无"
        #                 })

    def _format_addr(self, s):
        name, addr = parseaddr (s)
        return formataddr ((Header (name, 'utf-8').encode (), addr))

    def sendMail(self, responseResult,mailusers):
        print ("发送邮件")
        print (responseResult)
        # if not os.path.exists("%s/%s/%s.ipa" % (archivePath, targetName, targetName)):
        #     print("发送邮件 没有找到ipa文件")
        #     return
        #  <a href="itms-services://?action=download-manifest&url=https://www.pgyer.com/app/plist/74263d18d91273290c10fd0e32ff72bf>安装</a>
        # print(responseResult["appKey"])
        # msgInfo = "<html><body><table><tr><th>应用名称</th><th>%s</th></tr><tr><th>应用版本</th><th>%s</th></tr><tr><th>应用地址</th><th>https://www.pgyer.com/%s</th></tr><tr><th>应用更新时间</th><th>%s</th></tr></table><img src=%s width=\"150\" height=\"150\"></body></html>" % (
        #     responseResult["appName"], str (responseResult["appVersion"]), str (responseResult["appShortcutUrl"]),
        #     str (responseResult["appUpdated"]), str (responseResult["appQRCodeURL"]))
        msgInfo = "<h>测试测试的</h>"
        msg = MIMEText (msgInfo, 'html', 'utf-8')
        msg["Subject"] = MAIL_SUBJECT
        msg['From'] = self._format_addr ('iOS开发 <%s>' % MAIL_FROM)
        mailusers_str = ''
        for str in mailusers:
            mailusers_str+=self._format_addr(str)
            mailusers_str+=','

        print(mailusers_str)
        # msg['to'] = self._format_addr (' <%s>' % mailusers_str)
        msg['to'] = mailusers_str
        try:
            # // 创建一个SMTP对象
            server = smtplib.SMTP ()
            print (server)
            # // 通过connect方法链接到smtp主机
            server.connect (MAIL_HOST, "25")
            server.set_debuglevel (1)
            # // 启动安全传输模式
            # server.starttls()
            # // 登录邮箱
            # 校验用户，密码
            server.login (MAIL_FROM, Mail_PassWord)
            receivers = mailusers
            print(receivers)
            # // 发送邮件
            server.sendmail (MAIL_FROM, receivers, msg.as_string ())
            server.quit ()
            # 发送成功并打印
            print ("邮件发送成功 \n发送人:%s\n发送内容:\n%s接收者:%s " % (MAIL_FROM, msg, mailusers))
            return  1
        except Exception as e:
            print ("邮件发送失败：" + str (e))
            return 0









class MainWindow:
    def __init__(self):


        # define window

        self.frame = tkinter.Tk()
        self.frame.title("Xcode Bulid")
        self.frame.geometry("500x500")

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.py'
        options['filetypes'] = [('all files', '.*'), ('text files', '.xcodeproj'),('text files', '.xcworkspace')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.frame
        options['title'] = 'This is a title'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        # options['message'] = 'message'

        # if you use the multiple file version of the module functions this option is set automatically.
        # options['multiple'] = 1

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = self.frame
        options['title'] = 'This is a title'

        #define  select target file


        self.target_btn = tkinter.Button (self.frame, text="选择目标文件", width=60, height="1", bg='gray',
                                         command=self.askopenfilename)
        # self.target_btn.pack (**button_opt)
        self.target_btn.grid(row=0, column=0,columnspan=2)

       # define select build type
        self.dev_btn_v = tkinter.IntVar()

        # define 0 flag dev 1 flag dis
        self.buildtype = 1

        self.dev_btn = tkinter.Radiobutton(self.frame,text="dev",width=30,variable=self.dev_btn_v,value=0,command=self.selectBtnBuildType,bg="gray")
        self.dis_btn = tkinter.Radiobutton(self.frame, text="dis",width=30,variable=self.dev_btn_v,value=1,command=self.selectBtnBuildType,bg="gray")
        self.dev_btn.grid(row=1, column=0)
        self.dis_btn.grid (row=1, column=1)


        #define dev_taginfo
        self.label_desc = tkinter.Label (self.frame, text="版本描述:(选填)", width=30)
        self.taginfo_text = tkinter.Text (self.frame,width=40, height="1", bg='gray')
        self.label_desc.grid(row=2, column=0)
        self.taginfo_text.grid(row=2, column=1)

        #define mailto
        self.mail_desc = tkinter.Label (self.frame, text="测试人员邮箱(可多选)", width=60)
        self.mail_desc.grid (row=3, column=0,columnspan=2)



        # define tester ui tester

        i = 0
        for tester in MAILS_TESTER:

            variable = tkinter.IntVar()
            testerBtn = tkinter.Checkbutton(self.frame,text=tester['name'], width=20,
                                            variable = variable,
                                            # onvalue='t',
                                            # offvalue='f',
                                            command=self.createTesterBtn)
            testerBtn.grid(row=4 + int(i/2), column=i%2)
            i += 1
            MAILS_TESTER_BTN_ARR.append(variable)





        last_row = 4+int(i/2)+1
        # define start build btn
        self.build_btn = tkinter.Button (self.frame, text="开始打包", width=60, height="1", bg='gray',
                                          command=self.startbuild)

        self.build_btn.grid(row=last_row, column=0,columnspan=2)

        # define stop build btn
        self.cancle_build_btn = tkinter.Button (self.frame, text="结束打包", width=60, height="1", bg='gray',
                                         command=self.stopbuild)

        self.cancle_build_btn.grid (row=last_row+1, column=0, columnspan=2)









        self.frame.mainloop ()

    def createTesterBtn(self):
        for i in range(0, len(MAILS_TESTER_BTN_ARR)):
            btn_var = MAILS_TESTER_BTN_ARR[i]

            if(btn_var.get() == 1):
                if(MAILS_TESTER[i]["mail"] in MAILS_TESTER_SELECTER):
                    print(MAILS_TESTER[i]["mail"] + "数组中已存在")
                else:
                    MAILS_TESTER_SELECTER.append(MAILS_TESTER[i]["mail"])
            else:
                if (MAILS_TESTER[i]["mail"] in MAILS_TESTER_SELECTER):
                    MAILS_TESTER_SELECTER.remove(MAILS_TESTER[i]["mail"])





        print(MAILS_TESTER_SELECTER)

    def askopenfilename(self):
        """
         handle event
        """
        print(self.file_opt)
        print(tkinter.filedialog)
        # get filename
        self.filename = tkinter.filedialog.askopenfilename (**self.file_opt)
        print (self.filename)
        # get dirname and filename from filepath
        if(self.filename):
            self.filepath = os.path.dirname (self.filename)
            self.targetname = os.path.splitext(os.path.basename(self.filename))[0]
            [fname,fename]= os.path.splitext(self.filename)
            # 0 is project 1 is workspace
            if fename == ".xcworkspace":
                self.targettype = 1
            else:
                self.targettype = 0

            print(fname)
            print(fename)
            print(self.filepath)
            print("targetnames:   " + self.targetname)
            self.target_btn["text"] = str(self.filename)

    def selectBtnBuildType(self):
        if self.dev_btn_v.get() == 0:
            self.buildtype = 0

        else:
            self.buildtype = 1


        print(self.buildtype)
        print(self.taginfo_text.get(0.0,tkinter.END))

    def stopbuild(self):
        print("停止")
        os.system("exit()")


    def startbuild(self):
        print("开始打包");

        ipahelper = IPAHelper()

        # self.filepath = os.getcwd()
        # ipahelper.sendMail({"appName": "HD",
        #                 "appVersion": "appVersion",
        #                 "appShortcutUrl": "暂无",
        #                 "appUpdated": "暂无",
        #                 "appShortcutUrl":"暂无",
        #                 "appUpdated":"------",
        #                 "appQRCodeURL":"........"
        #                 },str(self.mail_text.get(0.0,tkinter.END)))
        #
        # self.build_btn.config (state=tkinter.DISABLED)
        # self.build_btn.config (state=tkinter.ACTIVE)
        # return
        if not os.path.exists(self.filepath):
            print("文件不存在")
            return


        archivePath = self.filepath + "/build"




        # 删除之前残留的资源
        if  os.path.exists(archivePath):
            shutil.rmtree (archivePath)


        ipapath     = "%s/%s/%s.ipa" % (archivePath, self.targetname, self.targetname)
        #cleanProject

        ok = ipahelper.cleanProject(self.targettype, self.filepath, self.targetname)
        if ok == 0:
            print("clean success")

            buildok = ipahelper.buildProject(self.targettype,self.filepath,self.targetname,archivePath)
            if buildok == 0:
                print("build ok")
                self.build_btn.config(text="build ok");
                archiveok = ipahelper.cerateIPA(self.buildtype,self.filepath,self.targetname,archivePath)
                if archiveok == 0:
                    print ("archive success")
                    if self.buildtype == 1:
                        # ,archivePath,filename,tagdesc,mailusers):
                        uploadok = ipahelper.uploadToPGY(archivePath, self.targetname, str(self.taginfo_text.get(0.0,tkinter.END)),MAILS_TESTER_SELECTER)
                        if uploadok == 0:
                            print("上传成功")
                            self.build_btn.config (state=tkinter.ACTIVE, text="上传成功")
                        else:
                            print("上传失败")
                            self.build_btn.config (state=tkinter.ACTIVE, text="上传失败")
                    else:
                        ipahelper.uploadToItunesConnect(archivePath,self.targetname)


                else:
                    self.build_btn.config (state=tkinter.ACTIVE, text="archiv failure")
                    print("archiv failure")
            else:
                self.build_btn.config (state=tkinter.ACTIVE, text="build failure")
                print("build failure")

        else:
            self.build_btn.config (state=tkinter.ACTIVE,text="clean failure")
            print("clean failure")






if __name__ == '__main__':
    frame = MainWindow ()