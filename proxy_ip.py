import re
import requests
import bs4


def open_url():
    url = "http://cn-proxy.com/"

    # 使用本地1082端口的代理，如有不同，更改所使用的端口即可
    proxies = {"http":"127.0.0.1:1082", "https":"127.0.0.1:1082"}

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.6.2000'}

    res = requests.get(url, headers = headers, proxies = proxies).content.decode("utf-8")

    # print(res.text)

    return res

def get_all_ip(res):
    # 获取到页面上所有的代理IP信息

    soup = bs4.BeautifulSoup(res, "html.parser")
    targets = soup.find_all('td')

    compile_ip = re.compile( r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])')
    re_num = re.compile(r'[0-9]{2,4}')
    re_year = re.compile(r'2018-')

    ips = []
    ports = []
    for each in targets:
        if compile_ip.match(each.text):
            ips.append(each.text)
  
        elif re_num.match(each.text):
            if re_year.match(each.text):
                pass
            else:
                ports.append(each.text)


    i = 0
    ip_all = []
    while i < len(ips):
        ip_all.append(ips[i]+":"+ports[i])
        # print(ips[i]+":"+ports[i])
        i = i + 1

    return ip_all

def get_avi_ip(ip_all):
    # 对获取到的IP进行测试，筛选掉无法连接或速度过慢的代理IP
    
    url='http://www.whatismyip.com.tw'

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.6.2000'}


    for each in ip_all:
        try:
            proxies = {"http":each}
            res = requests.get(url, proxies=proxies, headers=headers, timeout=(3,3))
            print(res)         
            print(proxies)
            
        except requests.exceptions.ConnectTimeout:
            NETWORK_STATUS = False
            print(each+"请求超时")
        
        except:
            print(each+"无法使用")
        else:
            # 将能够正常使用的代理IP写入.txt文件
            print(each+"连接正常")

            file = open("可用的代理IP.txt", "a", encoding = 'utf-8')
            file.write(each+"\n")
            file.close
    
   
def main():
    res = open_url()
    ip_all = get_all_ip(res)
    ip_avi = get_avi_ip(ip_all)

    print("获取完成")

    
if __name__ == "__main__":
    main()
