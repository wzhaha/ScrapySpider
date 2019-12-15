# -*- coding: utf-8 -*-
import scrapy


class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    start_urls = ['http://jandan.net/ooxx']

    def parse(self, response):
        item = {}
        item['image_urls'] = response.xpath('//img//@src').extract()  # 提取图片链接
        print(item)
        yield item

