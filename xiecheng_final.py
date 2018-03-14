import requests
import bs4
import re
import time
import os
import random
import pymssql

# 获取景点的详细信息
def open_url(page, head_datas, name):
    # 访问源
    host = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
   
    # 浏览器头部信息
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36}',
               'Referer':'http://you.ctrip.com/sight/chongming571/5681.html',
               'Cookie':'StartCity_Pkg=PkgStartCity=2; _abtest_userid=e74c1d70-50d9-43c3-8c86-0b21452c223f; UM_distinctid=16155888ba7a2-07430e799076d7-4353468-144000-16155888ba82fc; _RSG=mIa4qcNeaO2oqJerQlY88A; _RDG=28496414ac40d72e9532746a41ac46f315; _RGUID=2624a179-b412-44b0-a208-8af6b5a13d32; _ga=GA1.2.1140136322.1517558470; MKT_Pagesource=PC; CNZZDATA1256793290=157138234-1517557503-http%253A%252F%252Fwww.ctrip.com%252F%7C1517557503; bdshare_firstime=1517558477763; Customer=HAL=ctrip_gb; _gid=GA1.2.1290549758.1518148629; appFloatCnt=4; manualclose=1; ASP.NET_SessionSvc=MTAuOC4xODkuNTN8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUxMTI1OTIwNzU5NQ; _RF1=116.224.215.31; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1518782732056; __zpspc=9.4.1518177932.1518177932.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.443470209.1517558469937.1518148629385.1518177932087.1518148629385.1518177932087.0.0.0.4.4; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1518177945508%7D%5D; _bfi=p1%3D290510%26p2%3D290510%26v1%3D12%26v2%3D11; _bfa=1.1517558467111.2j1um.1.1518148624801.1518177680566.4.21; _bfs=1.11',
               'Content-Type':'application/x-www-form-urlencoded',
               'Accept-Encoding':'gzip, deflate',
               }
    
    # 景点游标信息
    data = head_datas

   
    # 获取代理IP
    file = open("可用的代理IP.txt")
    all_lines = file.readlines()
    
    file = open("可用的代理IP.txt")
    all_lines = file.readlines()
    ips = []
    
    
    for line in all_lines:
        ips.append(line.split())


    proxies = {"http":(random.choice(ips))[0]}
    print("\n\n\n\n\n正在使用"+str(proxies))

    fail = False
    
    # 访问携程
    try:
        res = requests.post(host, headers=headers, data=data, proxies=proxies, timeout=2)
        res = res.content.decode('utf-8')
        if res == "":
            fail = True
            print("返回故障，重新获取中")
    except:
        print(str(proxies)+"连接故障，重新尝试中")
        fail = True
    else:
        soup = bs4.BeautifulSoup(res, 'lxml')
        fail_content = get_info(soup, name)
        if fail_content == True:
            fail = True
        return fail


def get_info(soup, name):
    print("开始处理信息——")
    # 获取用户名
    users = []
    targets = soup.find_all("span", class_="ellipsis")
    for each in targets:
        try:
            if each.a['itemprop'] == "":
                pass
            else:
                users.append(each.a['title'])
                # users.append('用户名：%s' %each.a['title'])
                # print(each.a['title'])
        except:
            pass

    # 获取评论内容，去除空格和换行
    comments = []
    targets = soup.find_all("span", class_="heightbox")
    for each in targets:
        comments.append(each.text.replace("\n",""))
        # comments.append(' 评论：%s' %each.text.replace("\n",""))
        # print(each.text)

    # 虎丘总分评价
    avg_marks = []
    targets = soup.find_all("span", itemtype="http://schema.org/Rating")
    for each in targets:
        if str(each.span)[21:22] == '%':
            avg_marks.append(str(each.span)[19:21])
            # avg_marks.append(' 总分：'+str(each.span)[19:21])
            # print(str(each.span)[19:21])
        else:
            avg_marks.append(str(each.span)[19:22])
            # avg_marks.append(' 总分：'+str(each.span)[19:22])
            # print(str(each.span)[19:22])

    # 获取评论时间
    times = []
    targets = soup.find_all("em", itemprop="datePublished")
    for each in targets:
        # print(each.text)
        times.append(each.text)

    # 汇总在一起，一行数据为一个用户的内容
    result = []
    length = len(users)
    print(length)

  
    # 写入文件
    server = "localhost"
    user = "sa"
    password = "password."
    database = "Ctrip"
    

    for i in range(length):
        username = users[i]
        usercomment = comments[i]
        score = avg_marks[i]
        time = times[i]
        # 连接数据库，写入数据
        try:
            conn = pymssql.connect(server, user, password, database)
            cursor = conn.cursor()
            SQL = "insert into origin (username, destination, usercomment, score, time, platform) values ('{0}', '{1}', '{2}', {3}, '{4}', '{5}')".format(username, name, usercomment, score, time, "携程")
            # print(SQL)
            cursor.execute(SQL)
            conn.commit()
            conn.close()
        except:
            file = open(name+"ERROR.txt", "a", encoding = 'utf-8')
            file.write(SQL)
            file.close()
        else:
            pass
        
        print("完成第"+str(i+1)+"条评论获取")
        # file.close()

    # 获取失败的判断，获取到的数组长度为0  
    fail_content = False
    if length == 0:
        fail_content = True
        return fail_content

        

# 获取评论总页数
def get_max_page_num(url):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36}',
               'Cookie':'StartCity_Pkg=PkgStartCity=2; _abtest_userid=e74c1d70-50d9-43c3-8c86-0b21452c223f; UM_distinctid=16155888ba7a2-07430e799076d7-4353468-144000-16155888ba82fc; _RSG=mIa4qcNeaO2oqJerQlY88A; _RDG=28496414ac40d72e9532746a41ac46f315; _RGUID=2624a179-b412-44b0-a208-8af6b5a13d32; _ga=GA1.2.1140136322.1517558470; MKT_Pagesource=PC; CNZZDATA1256793290=157138234-1517557503-http%253A%252F%252Fwww.ctrip.com%252F%7C1517557503; bdshare_firstime=1517558477763; Customer=HAL=ctrip_gb; _gid=GA1.2.1290549758.1518148629; appFloatCnt=4; manualclose=1; ASP.NET_SessionSvc=MTAuOC4xODkuNTN8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUxMTI1OTIwNzU5NQ; _RF1=116.224.215.31; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1518782732056; __zpspc=9.4.1518177932.1518177932.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.443470209.1517558469937.1518148629385.1518177932087.1518148629385.1518177932087.0.0.0.4.4; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1518177945508%7D%5D; _bfi=p1%3D290510%26p2%3D290510%26v1%3D12%26v2%3D11; _bfa=1.1517558467111.2j1um.1.1518148624801.1518177680566.4.21; _bfs=1.11',
               'Content-Type':'application/x-www-form-urlencoded',
               'Accept-Encoding':'gzip, deflate',
               }

    res = requests.get(url, headers=headers)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    max_page_num = soup.find('b', class_="numpage").text

    return int(max_page_num)

# 获取景点的游标id
def get_head_datas(page, url):


    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36}',
               'Cookie':'StartCity_Pkg=PkgStartCity=2; _abtest_userid=e74c1d70-50d9-43c3-8c86-0b21452c223f; UM_distinctid=16155888ba7a2-07430e799076d7-4353468-144000-16155888ba82fc; _RSG=mIa4qcNeaO2oqJerQlY88A; _RDG=28496414ac40d72e9532746a41ac46f315; _RGUID=2624a179-b412-44b0-a208-8af6b5a13d32; _ga=GA1.2.1140136322.1517558470; MKT_Pagesource=PC; CNZZDATA1256793290=157138234-1517557503-http%253A%252F%252Fwww.ctrip.com%252F%7C1517557503; bdshare_firstime=1517558477763; Customer=HAL=ctrip_gb; _gid=GA1.2.1290549758.1518148629; appFloatCnt=4; manualclose=1; ASP.NET_SessionSvc=MTAuOC4xODkuNTN8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUxMTI1OTIwNzU5NQ; _RF1=116.224.215.31; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1518782732056; __zpspc=9.4.1518177932.1518177932.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.443470209.1517558469937.1518148629385.1518177932087.1518148629385.1518177932087.0.0.0.4.4; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1518177945508%7D%5D; _bfi=p1%3D290510%26p2%3D290510%26v1%3D12%26v2%3D11; _bfa=1.1517558467111.2j1um.1.1518148624801.1518177680566.4.21; _bfs=1.11',
               'Content-Type':'application/x-www-form-urlencoded',
               'Accept-Encoding':'gzip, deflate',
               }

    res = requests.get(url, headers=headers).content.decode('utf-8')


    var_resourceid = res.find("var resourceid")
    end = res.find('\"',var_resourceid + 18, var_resourceid + 60)
    resourceid = res[var_resourceid + 18: end]


    var_resourcetype = res.find("var resourcetype")
    end = res.find('\"',var_resourcetype + 20, var_resourcetype + 60)
    resourcetype = res[var_resourcetype + 20: end]

    var_districtid = res.find("var districtid")
    end = res.find('\"',var_districtid + 18, var_districtid + 60)
    districtid = res[var_districtid + 18: end]

    var_districtename = res.find("var districtename")
    end = res.find('\"', var_districtename +21, var_districtename + 60)
    districtename = res[var_districtename + 21: end]

    star = 0

    tourist = 0.0

    order = 3.0

    var_poiid = res.find("var poiid")
    end = res.find('\"', var_poiid + 13, var_poiid + 60)
    poiid = res[var_poiid + 13: end]

    page = page

    resoucetype = 2


    data = {"poiID":int(poiid),
            "districtId":int(districtid),
            "districtEName":districtename,
            "pagenow":page,
            "order":order,
            "star":star,
            "tourist":tourist,
            "resourceId":int(resourceid),
            "resoucetype":resoucetype,
            }

    # print(data)
    return(data)


def get_name(url):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36}',
               'Cookie':'StartCity_Pkg=PkgStartCity=2; _abtest_userid=e74c1d70-50d9-43c3-8c86-0b21452c223f; UM_distinctid=16155888ba7a2-07430e799076d7-4353468-144000-16155888ba82fc; _RSG=mIa4qcNeaO2oqJerQlY88A; _RDG=28496414ac40d72e9532746a41ac46f315; _RGUID=2624a179-b412-44b0-a208-8af6b5a13d32; _ga=GA1.2.1140136322.1517558470; MKT_Pagesource=PC; CNZZDATA1256793290=157138234-1517557503-http%253A%252F%252Fwww.ctrip.com%252F%7C1517557503; bdshare_firstime=1517558477763; Customer=HAL=ctrip_gb; _gid=GA1.2.1290549758.1518148629; appFloatCnt=4; manualclose=1; ASP.NET_SessionSvc=MTAuOC4xODkuNTN8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUxMTI1OTIwNzU5NQ; _RF1=116.224.215.31; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1518782732056; __zpspc=9.4.1518177932.1518177932.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.443470209.1517558469937.1518148629385.1518177932087.1518148629385.1518177932087.0.0.0.4.4; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1518177945508%7D%5D; _bfi=p1%3D290510%26p2%3D290510%26v1%3D12%26v2%3D11; _bfa=1.1517558467111.2j1um.1.1518148624801.1518177680566.4.21; _bfs=1.11',
               'Content-Type':'application/x-www-form-urlencoded',
               'Accept-Encoding':'gzip, deflate',
               }
    res = requests.get(url, headers=headers).content.decode('utf-8')
    soup = bs4.BeautifulSoup(res, 'html.parser')
    name = soup.find("div", class_="dest_toptitle detail_tt")
    # print(name.div.div.h1.text)
    return(name.div.div.h1.text)


# 主程序
def main():
    url = input("请输入需要爬取的景点链接：")
    page_num = get_max_page_num(url)
    name = get_name(url)
   
    i = 1
    while i <= page_num:
        head_datas = get_head_datas(i, url)
        fail = open_url(i, head_datas, name)
        if fail == False:
            print("已完成"+str(i)+"页的爬取工作")
            time.sleep(0.5)
            i = i+1
        else:
            i = i
      

if __name__=="__main__":
    main()
