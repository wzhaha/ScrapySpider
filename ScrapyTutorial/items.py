# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose,Join

"""
    Field 字段事实上有两个参数：
    第一个是输入处理器（input_processor） ，当这个item，title这个字段的值传过来时，可以在传进来的值上面做一些预处理。
    第二个是输出处理器（output_processor） ， 当这个item，title这个字段被预处理完之后，输出前最后的一步处理。
    scrapy内置的处理器:
        TakeFirst: 是Scrapy提供的内置处理器，用于提取List中的第一个非空元素
        MapCompose: 能把多个函数执行的结果按顺序组合起来，产生最终的输出，通常用于输入处理器
        Identity: 最简单的处理器，不进行任何处理，直接返回原来的数据。无参数
        Join: 返回用分隔符连接后的值。分隔符默认为空格。不接受Loader contexts。
        Compose: 用给定的多个函数的组合，来构造的处理器。list对象（注意不是指list中的元素），依次被传递到第一个函数，然后输出，
            再传递到第二个函数，一个接着一个，直到最后一个函数返回整个处理器的输出。默认情况下，当遇到None值（list中有None值）的时候
            停止处理。可以通过传递参数stop_on_none = False改变这种行为。
        
    
    每个字段的数据的处理过程是：
    第一步， 通过 add_xpath(), add_css() 或者 add_value() 方法)，提取到数据。
    第二步，将提取到的数据，传递到输入处理器（input_processor）中进行处理，处理结果被收集起来，并且保存在ItemLoader内（但尚未分配给该Item）。
    第三步，最后调用输出处理器（output_processor）来处理之前收集到的数据（这是最后一步对数据的处理）。然后再存入到Item中，输出处理器的结果是被分配到Item的最终值｡
    第四步，收集到所有的数据后, 调用ItemLoader.load_item() 方法来填充，并得到填充后的 Item 对象。
"""

class ScrapytutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class Author(scrapy.Item):
    birthdate = scrapy.Field(serializer=str)
    name = scrapy.Field()
    bio = scrapy.Field()


class CssItem(scrapy.Item):
    # 转换前是list，转换后是str
    title = scrapy.Field(
        # input_processor=MapCompose(date_convert),这里可以写自己的处理方法
        output_processor=TakeFirst()
    )
    imgUrl = scrapy.Field(
        input_processor=Join(),
        output_processor = TakeFirst()
    )
    imgText = scrapy.Field()
