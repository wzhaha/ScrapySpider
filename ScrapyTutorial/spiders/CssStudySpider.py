# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import *

class CssstudyspiderSpider(scrapy.Spider):
    name = 'CssStudySpider'
    start_urls = ['https://docs.scrapy.org/en/latest/_static/selectors-sample1.html']

    def parse(self, response):
        # # 基本的元素选择
        # item = {}
        # # title::text 选择子代的子文本节点 <title> 元素
        # item['title'] = response.css('title::text').get()
        # # href*=image，意思是a的href属性中包含了image这个字符串
        # item['aUrl'] = response.css('a[href*=image]::attr(href)').getall()
        # # *::text 选择当前选择器上下文的所有子代文本节点，此处选择了images里面的所有节点的text
        # item['image Text'] = [item.strip() for item in response.css('#images *::text').getall() if item.strip() is not '']
        #
        # # 元素的属性选择：1）xpath 2）css 3）自带.attrib
        # item['imgUrlXpath'] = response.xpath("//img/@src").getall()
        # item['imgUrlCss'] = response.css('img::attr(src)').getall()
        # item['imgYrlAttrib'] = [i.attrib for i in response.css('img')]
        #
        # # xpath表达式中的变量,用于查找 <div> 包含五个的标签 <a> 孩子们
        # item['imgCountId'] = response.xpath('//div[count(a)=$cnt]/@id', cnt=5).get()
        # green_print(item)
        #
        # yield item

        # if "docs" in response.url:
        #     from scrapy.shell import inspect_response
        #     inspect_response(response, self)


        # 项目加载器的使用
        # 首先，声明项目加载器, 第一个参数必须是实例化的对象
        cssItemLoader = ItemLoader(item=CssItem(), response=response)
        # 提取信息
        cssItemLoader.add_css('title','title::text')
        cssItemLoader.add_css('imgUrl', 'img::attr(src)')
        # 直接给字段赋值，尤其需要注意，不管赋值的数据是什么，都会自动转换成list类型
        cssItemLoader.add_value('imgText', response.css('a::text').getall())

        # 将提取好的数据load出来, 观察一下，发现三种方式填充的数据，均为List类型
        cssItemInfo = cssItemLoader.load_item()

        yield cssItemInfo







