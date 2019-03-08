# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
import requests
from ..items import ProxyItem
import logging

FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

class GetproxySpider(scrapy.Spider):
    name = 'getproxy'
    allowed_domains = ['xicidaili.com']
    start_urls = []
    for i in range(1, 10):
        start_urls.append('https://www.xicidaili.com/nn/{}'.format(i))

    def parse(self, response: HtmlResponse):
        ip = response.xpath('//tr[@class="odd"]//td[2]/text()').extract()
        port = response.xpath('//tr[@class="odd"]//td[3]/text()').extract()
        proxy_type = response.xpath('//tr[@class="odd"]//td[6]/text()').extract()
        proxies = zip(ip, port, proxy_type)
        for ip, port, proxy_type in proxies:
            proxy = {proxy_type: '{}://{}:{}'.format(proxy_type.lower(), ip, port)}
            try:
                resp = requests.get('https://cn.bing.com/', proxies=proxy, timeout=2)
                if resp.status_code == 200:
                    item = ProxyItem()
                    item['proxy'] = proxy
                    yield item
            except Exception as e:
               logging.info(e)