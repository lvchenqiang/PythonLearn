#coding=utf-8

import time
import hashlib
import requests
import json
# import urllib2
import random
def md5(s):
    m = hashlib.md5(s.encode("utf8"))
    return m.hexdigest()

def push_unicast(appkey, app_master_secret, device_token):
    timestamp = int(time.time() * 1000 )
    method = "POST"
    url = "http://msg.umeng.com/api/send"
    params = {"appkey": appkey,
              "timestamp": timestamp,
              "device_tokens": device_token,
              "type": "listcast",
# ========================消息体===========================
              "payload": {"aps":{
                                 "alert":str(random.random()),
                                 # # # # "badge":100,
                                 "content-available" : 1
                                 # "recall": "uu07360151565675199411"
                                },
                  "message_info": "{\"taskImageUrl\": \"http://member.ellabook.cn/2f5a8cbb45bf4c209f38ac0b0b0668ec\",\n\t\"taskDesc\": \"书籍分享（生日派对）\",\n\t\"taskStatus\": \"point\"\n,\"targetPage\":\"ellabookHD://task.wall\"}",
                  "message_type": "TASK_MESSAGE_REMINDING",


              },
# ========================消息体===========================
              "production_mode":"false"
    }
    post_body = json.dumps(params)

    sign = md5("%s%s%s%s" % (method,url,post_body,app_master_secret))
        # r = urllib2.urlopen(url + "?sign="+sign, data=post_body)
    response = requests.post(url + "?sign="+sign, data=post_body)
    print (response.json ())


if __name__ == "__main__":
    appkey = "59b9012da325116bc300054d"
    app_master_secret = "lukpzql5zqtprpf1n7lybqqyywjrmgbz"
    # device_token = "bcdda3c426336ac7fb43cf02fa38f251613b5a79aa9990fbc907d4429b8faa2b"
    # 31027506b8c6721bc9e4c4b45ded2555b48168eab0441c72e4408851697cf14a
    device_token = "e2fd659d02b67199402dd84ce256603e3fa2f0789e3be742a9f1cf7e06b3f3b8"

    # iphone
    # appkey = "579702b2e0f55addc7003443"
    # app_master_secret = "ug0qsj6ndrnkpdlnwmrprp2q7eyzbwfp"
    # device_token = "31f1ace7ce7a459300b32873bffd5e38ca0b74aaf8a36acab64d75b8720f40be"
    # for i in range(1,10):
    push_unicast(appkey, app_master_secret, device_token)
