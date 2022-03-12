import json
import re
from lxml import etree
from selenium import webdriver
from requests import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import getpass
import time
import keyboard
sz_cps=[]
sz_index=1
class key(object):

    def __init__(self,web,sz_cps,sz_index):
        self.web=web
        self.sz_cps = sz_cps
        self.sz_index = sz_index
        super(key, self).__init__()

    def test_a(self):

        url="https://bbs.125.la/"+self.sz_cps[self.sz_index][0]
        if len(self.sz_cps)>=self.sz_index:
            self.web.get(url)
            self.sz_index+=1
        print('a')

    def testing(self):
        keyboard.add_hotkey('f7', self.test_a)
        #keyboard.add_hotkey('ctrl+alt', print, args=('b'))
        keyboard.wait()

header_dd373_save=\
    {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'content-type': 'application/json; charset=utf-8',
'referer': 'https://bbs.125.la/forum.php?mod=forumdisplay&fid=178&filter=typeid&typeid=351',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
'x-requested-with': 'XMLHttpRequest',
}

def chromedriver():
    driver_path=r'.\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    try:
        a1=r"--user-data-dir=C:\Users\\"
        a2=getpass.getuser()
        a3=r'\AppData\Local\Google\Chrome\User Data'
        path=a1+a2+a3
        chromeOptions.add_argument(path)  # 设置成用户自己的数据目录
        chromeOptions.add_argument('disable-infobars')
        chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation']);
        chromeOptions.add_experimental_option('w3c', False)
    except:
        print("请关闭相关浏览器")
    caps = DesiredCapabilities.CHROME
    caps = {
        'loggingPrefs': {
            'performance': 'ALL',
        }
    }

    wd=webdriver.Chrome(executable_path=driver_path,chrome_options=chromeOptions,desired_capabilities=caps)
    return wd

def get_wd_cookies(wd):
    ck=wd.get_cookies()
    ck=get_ck(ck)
    print("登录成功")
    time.sleep(1.5)
    return ck

def get_ck(ck):
    cook={}
    for oneCK in ck:
        cook[oneCK['name']]=oneCK['value']
    return cook

def get_jin(url,cook):
    cookie=''
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    header_dd373_save['cookie']=cookie
    res=get(url=url,headers=header_dd373_save)
    try:
        html=eval(res.text)
    except:
        return True,res.text
    if res.status_code==200:
        return True,html
    return False,html

if __name__=="__main__":
    driver=chromedriver()


    time.sleep(0.1)
    driver.get("https://bbs.125.la/forum.php?mod=forumdisplay&fid=178&filter=typeid&typeid=351")
    time.sleep(0.5)
    ck=get_wd_cookies(driver)
    page=1
    cps=[]
    while_pd=True
    while while_pd:
        while_pd, html = get_jin('https://bbs.125.la/plugin.php?id=diyforum&&mod=recruit&ac=getThreadList&typeid=351&cityid=12&salary=&treaid=&page=' + str(page) + '&t=' + str(int(round(time.time() * 1000))), ck)
        html = html['data'].replace("\n", "").replace("\r", "").replace("\/", "/")
        companys = re.findall('<tr><td class="o">(.*?)</td></tr>', html, re.S)
        for com in companys:
            url = re.findall('&nbsp;<a href="(.*?)" target="_blank">', com, re.S)
            name = re.findall('<td>公司/企业<br>(.*?)</td>', com, re.S)
            if len(url) > 0 and len(name) > 0 and [url[0], name[0]] not in cps:
                cps.append([url[0], name[0]])

        page += 1
        if page>=130:
            while_pd=False
    print("公司扫描完毕，获取公司招聘资料")
    for cp in cps:
        print(cp[0], cp[1])
        if "深圳" in cp[1]:
            sz_cps.append([str(cp[0]).replace('amp;',''),cp[1]])
        else:
            buer,cp_text=get_jin('https://bbs.125.la'+str(cp[0]).replace('amp;',''),ck)
            html_cp=etree.HTML(cp_text)
            text1=html_cp.xpath('string(//blockquote[@class="layui-elem-quote"])')
            if "深圳" in cp[1]:
                sz_cps.append([str(cp[0]).replace('amp;', ''), cp[1]])
    print("筛选完毕")
    json.dump(sz_cps,open('companys.json','w'),indent=4)
    key = key(driver,sz_cps,sz_index)
    key.testing()

