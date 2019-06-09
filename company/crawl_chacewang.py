import csv
import time
import re
import requests
import json
from pyquery import PyQuery as pq

all_url = 'http://www.chacewang.com/ProjectSearch/CopyIndex?citycode=RegisterArea_XNDQ_Sichuan_ChengDuShi'

header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'Hm_lvt_c83ad9c8bbe59cb2528a218a76c83594=1560060315; Hm_lvt_f9b4d143305c6f75248d93b7b5d8f6f1=1560060315; nb-referrer-hostname=www.chacewang.com; ASP.NET_SessionId=gezl5lwdod2ltks2edp4dnox; currentCity=DC7B72EC-92F0-4DB2-BFF2-BCE13D147592; nb-start-page-url=http%3A%2F%2Fwww.chacewang.com%2FProjectSearch%2FCopyIndex%3Fcitycode%3DRegisterArea_XNDQ_Sichuan_ChengDuShi; Hm_lpvt_f9b4d143305c6f75248d93b7b5d8f6f1=1560084381; Hm_lpvt_c83ad9c8bbe59cb2528a218a76c83594=1560084381',
'Host':'www.chacewang.com',
'Referer':'http://www.chacewang.com/?citycode=RegisterArea_XNDQ_Sichuan_ChengDuShi',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    
}
web_name = []
all_key = []
all_name = [
    '人才认定与资助', '知识产权', '创新载体', '贷款贴息贴保', '配套资助', '高新技术企业', '品牌与市场开拓',
    '事后资助', '扩产上规模', '重大项目', '新兴产业', '传统产业', '贸易物流', '中小微企业', '大型企业', '总部企业',
    '研发资助', '科研立项', '研发中试', '应用示范', '产业化', '技术改造', '节能减排', '信息化/两化融洽', '事前资助',
    '股权资助', '科技奖励', '标注化', '中介服务', '活动策划', '招商引资', '社会组织', '产业联盟', '产业基金'
]
all_resp = pq(requests.get(all_url, headers=header).text)
item_list = all_resp('ul.list.Crawler li').items()
for item in item_list:
    item_name = item.text()
    item_key = item.attr('data-key')
    all_key.append(item_key)
    web_name.append(item_name)
for real, web, key in zip(all_name, web_name, all_key):
    print(real, web)

    base_url = 'http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex=0&pageSize=20&cylb=&diqu=RegisterArea_XNDQ_Sichuan_ChengDuShi&bumen=&cylbName=&partition={}&partitionName={}&searchKey=&_=1560003902331'.format(key,web)
    print(base_url)
    page_re = json.loads(requests.get(base_url).text).get("total")
    allpage = int(page_re / 20) + 1
    for page in range(0, allpage):
        time.sleep(1)
        bases_url = 'http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex={}&pageSize=20&cylb=&diqu=RegisterArea_XNDQ_Sichuan_ChengDuShi&bumen=&cylbName=&partition={}&partitionName={}&searchKey=&_=1560003902331'.format(page,key,web)
        url = base_url.format(page)
        resp = requests.get(url).text

        data_lists = json.loads(resp).get("rows")
        # print(data_list)
        for item in data_lists:

            MainID = item.get("MainID")
            indexl_url = 'https://www.chacewang.com//WeChat/Mini/PeDetail?mainID={}&openid=e'.format(MainID)

            doc = pq(requests.get(indexl_url).text)
            name = doc("div.div-content div").eq(0).text()
            city = doc('span#subhead3').text()
            main_city = re.findall(re.compile(r'部门：(.*)'), str(city))[0]
            if '国' in city:
                loc_ = '中华人民共和国'
            if '省' in city:
                loc_ = re.findall(re.compile(r'部门：(.*?)省'), str(city))[0]
            if '市' in city:
                loc_ = re.findall(re.compile(r'部门：(.*?)市'), str(city))[0]
            if '区' in city:
                loc_ = re.findall(re.compile(r'部门：(.*?)区'), str(city))[0]
            if '县' in city:
                loc_ = re.findall(re.compile(r'部门：(.*?)县'), str(city))[0]

            post_time = doc('span#subhead4').text().replace('申报时间 ： ', '')

            with open('cha_reslut.csv', 'a', encoding='gb18030', newline='') as f:
                writer = csv.writer(f)
                writer.writerow((real, name, main_city, loc_, post_time))
            print(real, name, main_city, loc_, post_time)



# base_url = 'http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex={}&pageSize=20&cylb=&diqu=RegisterArea_XNDQ_Sichuan_ChengDuShi&bumen=&cylbName=&partition=&partitionName=&searchKey=&_=1559991476659'
#
# header = {'Accept':'application/json, text/javascript, */*; q=0.01',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
# 'Connection':'keep-alive',
# 'Content-Type':'application/json',
# 'Cookie':'Hm_lvt_c83ad9c8bbe59cb2528a218a76c83594=1559884091,1559915636; Hm_lpvt_c83ad9c8bbe59cb2528a218a76c83594=1559915636; Hm_lvt_f9b4d143305c6f75248d93b7b5d8f6f1=1559884091,1559915636; Hm_lpvt_f9b4d143305c6f75248d93b7b5d8f6f1=1559915636',
# 'Host':'www.chacewang.com',
# 'Referer':'http://www.chacewang.com/ProjectSearch/CopyIndex?citycode=RegisterArea_XNDQ_Sichuan_ChengDuShi',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
# 'X-Requested-With':'XMLHttpRequest',
#
# }
# # for page in range(0,90):
# #     time.sleep(1)
# #     url = base_url.format(page)
# #     resp = requests.get(url).text
# #
# #     data_list = json.loads(resp).get("rows")
# #     # print(data_list)
# #     for item in data_list:
# #
# #         MainID = item.get("MainID")
# #         indexl_url = 'https://www.chacewang.com//WeChat/Mini/PeDetail?mainID={}&openid=e'.format(MainID)
# #
# #         doc = pq(requests.get(indexl_url).text)
# #         name = doc("div.div-content div").eq(0).text()
# #         city = doc('span#subhead3').text()
# #         main_city = re.findall(re.compile(r'部门 ： (.*)'),str(city))[0]
# #         if '国' in city:
# #             loc_ = '中华人民共和国'
# #         if '省' in city:
# #             loc_ = re.findall(re.compile(r'部门 ： (.*?)省'),str(city))[0]
# #         if '市' in city:
# #             loc_ = re.findall(re.compile(r'部门 ： (.*?)市'), str(city))[0]
# #         if '区' in city:
# #             loc_ = re.findall(re.compile(r'部门 ： (.*?)区'), str(city))[0]
# #         if '县' in city:
# #             loc_ = re.findall(re.compile(r'部门 ： (.*?)县'), str(city))[0]
# #
# #         post_time = doc('span#subhead4').text().replace('申报时间 ： ','')
# #
# #         with open('cha_reslut.csv','a',encoding='gb18030',newline='') as f:
# #             writer = csv.writer(f)
# #             writer.writerow((name,main_city,loc_,post_time))
# #         print(name,main_city,loc_,post_time)