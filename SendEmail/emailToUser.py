#coding: utf-8
import requests
import email.utils
import email.parser
import smtplib
import os
import posixpath
import psutil
from email.mime.text import MIMEText

# 获取IP地址
ip = os.popen("ifconfig |grep -v 127 |grep inet |awk '{print $2}'|cut -d: -f2").read().strip()
print(ip)
hostname = os.popen("hostname").read().strip()
# 获取主机名
print(hostname)
# //获取CPU线程
cpu = psutil.cpu_count()
# 虚拟内存
print(psutil.virtual_memory())
# 内存使用率
print(psutil.disk_usage('/'))
# // 获取内存总量
# mem = os.popen("free -m |grep Mem |awk '{print $2}'").read().strip() + "M"
mem = str(psutil.disk_usage('/')[0]/1024/1024/1024) + "M"
print(mem)
# 获取硬盘总大小
# disk = os.popen("fdisk -l |grep -E Disk |awk '{print $3}'").read().strip() + "G"
disk = str(psutil.disk_usage('/')[0]/1024/1024/1024/1024) + "G"
# //指定使用网易163邮箱
HOST = "smtp.163.com"
# //邮件标题
SUBJECT = "hahahahah"
# //收件人
TO = "xxxxxxxn@gmail.com"
# //发件人
FROM = "1wewewe3@163.com"

Email_password = "123456"
msg = MIMEText("----hello, wo shzqeqweqweqweqweqweqweeljsidjfds sdf sdfs d.--------", 'plain', 'utf-8')
print(msg)

msg["Subject"] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

try:
    # // 创建一个SMTP对象
    server = smtplib.SMTP()
    print("服务")
    print(server)
    # // 通过connect方法链接到smtp主机
    server.connect(HOST, "25")
    server.set_debuglevel(1)
    # // 启动安全传输模式
    # server.starttls()
    # // 登录163邮箱
    # 校验用户，密码
    server.login(FROM, Email_password)
    # // 发送邮件
    server.sendmail(FROM, [TO], msg.as_string())

    server.quit()
    # 发送成功并打印
    print("邮件发送成功 %s %s %s %s %s" % (hostname, ip, cpu, mem, disk))

except Exception as e:
    print("邮件发送失败：" + str(e))


# https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432005226355aadb8d4b2f3f42f6b1d6f2c5bd8d5263000