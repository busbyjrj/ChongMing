import requests
import re
from bs4 import BeautifulSoup
import urllib
import pymssql

def hhh1(url):

    r=requests.get(url,timeout=30)
    r.encoding = r.apparent_encoding
    return r.text

def hhh2(url,liebiao):
        html=hhh1(url)
        soup=BeautifulSoup(html,'html.parser')
        name=soup.find_all('a',"ri-uname")
        time=soup.find_all('div',"ri-time")
        pingjia=soup.find_all('div',"ri-remarktxt")
        
        for i in range(len(pingjia)):
            pingjia2=[]
            pingjia3=''
            pingjia2.extend(pingjia[i].contents)
            for j in range(len(pingjia2)):
                pingjia3+=pingjia2[j].string.replace('\r','').replace('\n','')
            name1=name[i].attrs['title']
            time1=time[i].string
            liebiao.append([name1,time1,pingjia3])

   
def hhh3(liebiao,lujing):
    for i in liebiao:
        name_=i[0]
        time_=i[1]
        pingjia_=i[2]
        with open (lujing,'a',encoding='utf-8') as f:
            f.write(name_+'：  '+time_+'  '+pingjia_+'\n\n\n')
              
        server = "localhost"
        user = "sa"
        password = "password."
        database = "baidu"
        try:
            conn = pymssql.connect(server, user, password, database)
            cursor = conn.cursor()
            SQL = "insert into origin (username, destination, usercomment, time, platform) values ('{0}', '{1}', '{2}','{3}', '{4}')".format(name_, "崇明岛", pingjia_, time_, "百度旅游")
            # print(SQL+";\n")
            cursor.execute(SQL)
            conn.commit()
            conn.close()
        except:
            file = open("ERROR.txt", "a", encoding = 'utf-8')
            file.write(SQL)
            file.close()
        else:
            pass

def main():
    liebiao=[]
    lujing='D://chongming.doc'
    for i in range(34): 
        num=15*i
        url='https://lvyou.baidu.com/chongmingdao/remark/?rn=15&pn='+str(num)+'&style=hot#remark-container'
        hhh2(url,liebiao)
    hhh3(liebiao,lujing)

main()
