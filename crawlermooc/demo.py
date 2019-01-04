from typing import Dict, List, Any

import requests
import re
import os


class NetworkHandle(object):
    def __init__(self):
        print('开始爬取内容')

    # 获取网页的源代码
    def getsource(self, url):
        html = requests.get(url)
        return html.text

    # 获取起始页数
    def getAllLinks(self, url, total_page):
        startPage = int(re.search('page=(\d+)', url, re.S).group(1))
        allLinks = []
        for i in range(startPage, total_page):
            link = re.sub('page=\d+', 'page=%s' % i, url, re.S)
            allLinks.append(link)
        return allLinks

    def getInfo(self, html):
        titles = re.findall('<h3 class="course-card-name">(.*?)</h3>', html, re.S)
        cardPicUrls = re.findall('img class="course-banner lazy" data-original="(.*?)"', html, re.S)

        info = []

        if len(titles) != len(cardPicUrls):
            print("文件出错")

            return info
        else:
            print("文件解析")
            for i in range(0, len(titles)):
                tmp = {}
                print
                titles[i]
                print
                cardPicUrls[i]
                tmp["name"] = titles[i]
                tmp['pic'] = cardPicUrls[i]
                info.append(tmp)
            return info

    def saveinfo(self, iteminfo):
        print("开始写文件")
        # 以读写的方式打开
        fp = open("resource//info.txt", 'a')
        for each in iteminfo:
            fp.writelines('name: ' + each["name"] + '\n')
            fp.writelines('picurl: ' + each["pic"] + '\n')
            f = open('pic//' + os.path.basename(each["pic"]), 'wb')
            pic = requests.get("http:" + each["pic"])
            f.write(pic.content)
            f.close()
        fp.close()


if __name__ == '__main__':


    classinfo = []
    networkHandle = NetworkHandle()
    alllinks = networkHandle.getAllLinks('http://www.imooc.com/course/list?c=ios&page=1', 6)
    print(alllinks)
    for link_url in alllinks:
        print("开始处理页面")
        html = networkHandle.getsource(link_url)
        info: List[Dict[str, Any]] = networkHandle.getInfo(html)
        print(info)
        networkHandle.saveinfo(info)
