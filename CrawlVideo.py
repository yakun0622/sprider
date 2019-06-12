# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time


class ViedeoCrawler():
    def __init__(self):
        self.proxies = {'https': '127.0.0.1:1080'}
        self.url = "https://www.xvideos.com/video48168145/_"
        self.down_path = r"/Users/wangyakun/PycharmProjects/1024Video-Crawler/download"
        self.final_path = r"/Users/wangyakun/PycharmProjects/1024Video-Crawler/final"
        self.name = "uncensord"
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; MZ-m2 note Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/6.5.506 UWS/2.10.1.22 Mobile Safari/537.36'
        }

    def run(self):
        print("Start!")
        start_time = time.time()
        os.chdir(self.down_path)
        html = requests.get(self.url, proxies=self.proxies).text
        print('======== html ============')
        bsObj = BeautifulSoup(html, 'lxml')
        self.name = bsObj.title.string.replace(' ', '')
        titles = bsObj.select("body  script")  # CSS 选择器
        str = titles[5]
        list = str.contents[0].split(';')
        realPath = ''
        for line in list:
            if 'setVideoHLS' in line:
                realPath = line.split('\'')[1]
                break
        print(realPath.replace('hls.m3u8', 'hls-720p.m3u8'))
        urlPre = realPath.replace('hls.m3u8', '')
        resp = requests.get(urlPre + 'hls-720p.m3u8', proxies=self.proxies).text
        list = resp.split('\n')
        hlsList = []
        for hls in list:
            if 'hls' in hls:
                print(hls)
                hlsList.append(urlPre + hls)
        i = 1  # count
        for key in hlsList:
            if i % 50 == 0:
                print("休眠10s")
                time.sleep(10)
            try:
                resp = requests.get(key, headers=self.headers, proxies=self.proxies)
                print('request url===')
                print(key)
                print(resp)
            except Exception as e:
                print(e)
                return
            if i < 10:
                name = ('clip00%d.ts' % i)
            elif i > 100:
                name = ('clip%d.ts' % i)
            else:
                name = ('clip0%d.ts' % i)
            with open(name, 'wb') as f:
                f.write(resp.content)
                print('正在下载clip%d' % i)
            i = i + 1
        print("下载完成！总共耗时 %d s" % (time.time() - start_time))
        print("接下来进行合并……")
        os.system('cat %s/*.ts > %s%s.ts' % (self.down_path, self.final_path, self.name))
        print("合并完成，请您欣赏！")
        y = input("请检查文件完整性，并确认是否要删除碎片源文件？(y/n)")
        if y == 'y':
            files = os.listdir(self.down_path)
            for filena in files:
                del_file = self.down_path + '\\' + filena
                os.remove(del_file)
            print("碎片文件已经删除完成")
        else:
            print("不删除，程序结束。")


if __name__ == '__main__':
    crawler = ViedeoCrawler()
    crawler.run()