import urllib
import re
import sqlite3
import time
import random
from bs4 import BeautifulSoup
from urllib import request
from urllib import error

#保存数据至数据库
def saveData2DB(datalist, dbpath):
    int_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    print("正在保存爬取数据")
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+str(data[index])+'"'
        sql_info = '''insert into  comment(comment,name) 
                    VALUES(%s) 
            ''' % ",".join(data)
        # print(sql_info)
        cur.execute(sql_info)
        conn.commit()
    cur.close()
    conn.close()

#初始化数据库
def int_db(dbpath):
    sql = '''create table comment
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text,
                comment text
                )'''  # 创建数据库
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

#获取数据
def getData(baseurl):
    datalist = []
    for i in range(0,5):
        #转为字符串
        baseurl=str(baseurl)
        #获取baseurl中需要改变的地方
        url1=re.findall(url_module,baseurl)[0]
        #根据页数进行替换
        url=baseurl.replace(url1, "start={num}".format(num=i*20))
        html = askURL(url)
        print("正在解析url")
        time.sleep(random.random()*5)
    #    逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
    # class_表示web中的class类
        #找到网页中所有评论的父元素
        for item in soup.find_all('div', class_="comment"):
            # print(item)测试
            data = []  # 保存一部电影的全部信息
            print("item before str:",item)
            item = str(item)
            print("item after str:", item)
            #若评论或评论者名字为空就跳过
            # if len(re.findall(findCommentContent,item))==0 or len(re.findall(findName,item))==0 :
            #     continue
            #根据正则表达式获取评论
            comment = re.findall(findCommentContent, item)[0]
            comment=str(comment)
            comment.replace("\n","")
            # str1=re.findall(findCommentContent,item);
            #


            # 根据正则表达式获取评论者名称
            name=re.findall(findName,item)[0][1]
            data.append(comment)
            data.append(name)
            datalist.append(data)

    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Cookie": "ll='118282'; bid=EwSSRGmFsUg; __utmc=30149280; dbcl2='238649768:AaeIXb+2QPM'; ck=LBHa; push_noty_num=0; push_doumail_num=0; __utmv=30149280.23864; __yadk_uid=yxcHwxsb3G88SsQTY2nswv2a4Govn6N1; __gads=ID=52b226f675198a85-222e9032eec8005a:T=1622027988:RT=1622027988:S=ALNI_Majlgr60EwIsDkbjtCK3DvFvX28hg; __utmz=30149280.1622080069.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); douban-fav-remind=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1622164556%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _pk_id.100001.8cb4=88dd65c66126b55a.1621593592.5.1622164556.1622080302.; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.1227828915.1621593602.1622080069.1622164564.5; __utmt=1; __utmb=30149280.2.10.1622164564"
    }
    print("爬取开始")
    time.sleep(random.random() * 5)
    #  模拟浏览器头部信息，向头部豆瓣服务器发送消息
    # （伪装）用户代理，将一个伪装传给对方服务器，包含本机的机器类型、浏览器类型
    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req, timeout=5)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
# import xlwt
# def saveData(datalist, savepath):
#     print("正在保存爬取数据")
#     # 创建workbook对象
#     workbook = xlwt.Workbook(encoding="utf-8")
#     # 创建工作标单
#     worksheet = workbook.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)
#     # 写入数据
#     col = ("编号", "电影详情链接", "图片链接", "电影中文名称", "电影外文名称", "评分", "评价数", "概况")
#     for i in range(0, 7):
#         worksheet.write(0, i, col[i])
#     for i in range(0, 250):
#         print("当前已经爬取:%d条" % (i+1))
#         data = datalist[i]
#         for j in range(0, 7):
#             worksheet.write(i+1, j, data[j])
#     workbook.save(savepath)
#     print("爬取数据保存结束")


# 前面是为了方便函数模块化封装，实际上本页程序运行的时候没有调用任何函数
# 为了运行函数则需要在主程序中写

def mian():
    #要爬取的评论首页
    baseurl = "https://movie.douban.com/subject/34825976/comments?start=0&limit=20&status=P&sort=new_score"
    # saveData(datalist=getData(baseurl), savepath="豆瓣电影Top250.xls")
    #设置数据库名称
    dbpath = "comment.db"
    saveData2DB(datalist=getData(baseurl), dbpath=dbpath)

#正则表达式们
findLink = re.compile(r'<a href="(.*?)">', re.S)  # 创建正则表达式对象，表示规则（字符串模式）
findImageSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S是让换行符出现在表达式中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findScore = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudgePeopleNum = re.compile(r'<span>(\d*)人评价</span>', re.S)
findInq = re.compile(r'<span class="inq">(.*?)</span>', re.S)
findCommentContent = re.compile(r'<span class="short">([\s\S]*)</span>')
findName = re.compile(r'<a class="" href="(.*)">(.*)</a>')
url_module=re.compile(r'comments\?(.*)&limit')

if __name__ == '__main__':
    mian()
    print("成功")
