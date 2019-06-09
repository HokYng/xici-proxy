# import requests
# import re
# import datetime
# from bs4 import BeautifulSoup
# # # from test import headers
# #
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'Hm_lvt_c83ad9c8bbe59cb2528a218a76c83594=1559972544; Hm_lvt_f9b4d143305c6f75248d93b7b5d8f6f1=1559972544; nb-referrer-hostname=www.chacewang.com; ASP.NET_SessionId=oatnzlvxa3fy135efgcykpzh; currentCity=5a3209b2-f868-47fa-862a-15f5c1f950f4; Hm_lpvt_c83ad9c8bbe59cb2528a218a76c83594=1560005973; Hm_lpvt_f9b4d143305c6f75248d93b7b5d8f6f1=1560005973; nb-start-page-url=http%3A%2F%2Fwww.chacewang.com%2FProjectSearch%2FCopyIndex%3Fcitycode%3DRegisterArea_HNDQ_Guangdong_SZ',
#     'Host': 'www.chacewang.com',
#     'Referer': 'http://www.chacewang.com/NewHome/Index',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
# }
#
# response = requests.get('http://www.chacewang.com/ProjectSearch/CopyIndex?citycode=RegisterArea_HNDQ_Guangdong_SZ', headers=headers)
# # 如此可以看到项目类别了， 注意cookies的过期时间等
# print(response.text)
# print(response.cookies)
#
#
#
# print(datetime.datetime.fromtimestamp(1559972544))
# print(datetime.datetime.fromtimestamp(1560005973))
# print(datetime.datetime.now())

print(hex(0x23))