# proxy_ip.py 使用说明
**用途：**自动获取[一个免费提供国内代理ip的网站](http://cn-proxy.com/)上所有的代理ip数据，并连接一次测试可用程度，将成功连接的代理ip写入一个.txt文件，以供后续爬虫使用代理ip匿名。

# lvmama_final.py 使用说明
**用途：**输入想要爬取的景点首页地址，自动获取所有的用户名、评论内容、评论时间和评分信息，并写入本地 SqlServer 数据库中。
**注意：**驴妈妈的服务器容纳能力有限，高频率访问某个景点页面，会导致该景点的页面404无响应，本爬虫仅用于学习使用，不应当影响驴妈妈服务器的稳定性，故每爬取一页内容后会等待一定时间才获取下一页的内容。

# xiecheng_final.py 使用说明
**用途：**同上。
**注意：**本爬虫仅用于学习使用，不应当影响携程服务器的稳定性，故每爬取一页内容后会等待一定时间才获取下一页的内容。

# baidu_final.py 使用说明
**用途：**百度旅游的评论内容为静态页面，故本爬虫仅适用于本项目，其它项目仅供参考。
**注意：**本爬虫仅用于学习使用，不应当影响百度旅游服务器的稳定性，故每爬取一页内容后会等待一定时间才获取下一页的内容。

# 再次说明
**所有爬虫仅用于科学研究与学习用，本项目未对携程、驴妈妈和百度旅游的服务器或网络造成明显影响，并不会将所获取到的内容用于任何商业用途。其他人若使用本项目的源代码，也应当遵守这两点，请合理使用爬虫。