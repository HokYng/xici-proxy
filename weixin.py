import time
import re
import datetime
import json
import random
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymongo
import threading


class Spider:
    HOST = '127.0.0.1'
    PORT = 27017
    MONGODB = 'spider'
    USERNAME = '**********'
    PASSWORD = '**********'
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    ]

    def __init__(self):
        self.driver = Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.session = requests.Session()
        self.cookie = None
        self.token = None
        client = pymongo.MongoClient(self.HOST, self.PORT)
        db = client[self.MONGODB]
        if db.authenticate(self.USERNAME, self.PASSWORD):
            self.collection = db['wechat']

    def wechat_login(self, username, passwd):
        self.driver.get('https://mp.weixin.qq.com/')
        user = self.driver.find_element_by_name('account')
        password = self.driver.find_element_by_name('password')
        user.send_keys(username)
        password.send_keys(passwd)
        checkbox = self.driver.find_element_by_class_name('frm_checkbox_label')
        checkbox.click()
        login = self.driver.find_element_by_class_name('btn_login')
        login.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mp_header_account"]/div/div/span/div')))
        self.cookie = {item['name']: item['value'] for item in self.driver.get_cookies()}
        self.token = re.findall(r'token=(\d+)', self.driver.current_url)[0]

    def get_chat(self, query):
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        query_string = {
            'action': 'search_biz',
            'lang': 'zh_CN',
            'f': 'json',
            'query': query,
            'ajax': '1',
            'random': random.random(),
            'token': self.token,
            'begin': 0,
            'count': 5
        }
        while True:
            headers = {'User-Agent': random.choice(self.USER_AGENTS), 'HOST': 'mp.weixin.qq.com'}
            response = self.session.get(search_url, params=query_string, headers=headers, cookies=self.cookie)
            resp = json.loads(response.text)
            try:
                total = resp['total']
                for i in resp['list']:
                    # threading.Thread(target=self.get_content, args=(i, )).start()
                    self.get_content(i)
            except Exception as e:
                total = 0
                print(e)
            query_string['begin'] += query_string['count']
            if query_string['begin'] - total >= query_string['count']:
                break
            time.sleep(5)

    def get_content(self, i):
        content_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        query_string = {
            'action': 'list_ex',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'token': self.token,
            'fakeid': i['fakeid'],
            'type': '9',
            'begin': 0,
            'count': 5
        }
        while True:
            headers = {'User-Agent': random.choice(self.USER_AGENTS), 'HOST': 'mp.weixin.qq.com'}
            response = self.session.get(content_url, params=query_string, headers=headers, cookies=self.cookie)
            resp = json.loads(response.text)
            try:
                total = resp['app_msg_cnt']
                for appmsg in resp['app_msg_list']:
                    d = {}
                    d['update_time'] = datetime.datetime.fromtimestamp(appmsg['update_time'])
                    d['title'] = appmsg['title']
                    d['link'] = appmsg['link']
                    d['fakeid'] = query_string['fakeid']
                    self.collection.insert_one(d)
            except Exception as e:
                total = 0
                print(e, response.url)
            query_string['begin'] += query_string['count']
            if query_string['begin'] - total >= query_string['count']:
                break
            time.sleep(5)

    def close(self):
        self.session.close()
        self.driver.close()


if __name__ == '__main__':
    username = '*******@qq.com'
    passwd = '***********'
    spider = Spider()
    spider.wechat_login(username, passwd)
    spider.get_chat('python')
