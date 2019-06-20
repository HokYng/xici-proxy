# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import HtmlResponse
from ..items import ReviewItem, CommentItem


class CommentSpider(RedisCrawlSpider):
    name = 'comment'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    redis_key = 'comment:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r'https://movie.douban.com/top250\?start=\d+'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'^https://movie.douban.com/subject/\d+/$'), callback='parse_detail', follow=False),
    )

    def parse_item(self, response: HtmlResponse):
        for li in response.xpath('//ol[@class="grid_view"]/li'):
            item = ReviewItem()
            item['title'] = li.xpath('.//div[1]/a/span[1]/text()').extract_first()
            item['rate'] = li.xpath('.//div[2]/div/span[2]/text()').extract_first()
            item['quote'] = li.xpath('.//div[2]/p/span/text()').extract_first()
            yield item

    def parse_detail(self, response: HtmlResponse):
        print(response.url)
        item = ReviewItem()
        item['title'] = response.xpath('//h1/span/text()').extract_first()
        item['doctor'] = response.xpath('//*[@id="info"]/span[1]/span[2]//text()').extract_first()
        actor = response.xpath('//*[@id="info"]/span[3]/span[2]//text()').getall()
        item['actor'] = ''.join(actor)
        item['rating_per'] = response.xpath('//div[@class="item"][1]/span[last()]/text()').extract_first()
        item['num'] = response.xpath('//*[@id="content"]/div[1]/span[1]/text()').extract_first()
        yield item
        comments = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href').get()
        if comments:
            yield scrapy.Request(url=comments, callback=self.parse_short)

    def parse_short(self, response: HtmlResponse):
        item = CommentItem()
        item['title'] = response.xpath('//h1//text()').extract_first()
        for div in response.xpath('//div[@class="comment-item"]'):
            comment = div.xpath('./div[2]/p/span/text()').extract_first()
            item['comment'] = comment
            yield item
        next_page = response.xpath('//*[@id="paginator"]/a[last()]/@href').extract_first()
        if next_page:
            regex = re.compile(r'\?.*')
            next_page = regex.sub(next_page, response.url)
            yield scrapy.Request(url=next_page, callback=self.parse_short)
