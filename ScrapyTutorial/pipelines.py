# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import pymysql
from scrapy.mail import MailSender
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class ScrapytutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class QuotePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='123456',
                                       db='spider')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        # if item.get('author'):
        #     item['author'] = item['author']+' haha'
        #     return item
        # else:
        #     raise DropItem("Missing tag")
        # sql语句
        if item.get('author') and item.get('text') and item.get('tags'):
            insert_sql = """insert into quotes(author, text, tag) VALUES (%s,%s,%s)"""
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql, (item['author'], item['text'], item['tags']))
            # 提交，不进行提交无法保存到数据库
            self.connect.commit()
        else:
            raise DropItem('字段成分缺失')

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        if spider.name == 'quotes':
            self.file = open('ScrapyTutorial/out/out.txt', 'w')

    def close_spider(self, spider):
        if spider.name == 'quotes':
            self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item['author']) + "\n"
        self.file.write(line)
        return item

class NotificationPipline(object):

    def open_spider(self, spider):
        self.mailer = MailSender(smtphost='smtp.qq.com', mailfrom='1063373512@qq.com', smtpport=25, smtpuser='1063373512@qq.com', smtppass='ccbzuebgcsbobcjc')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        return self.mailer.send(to=['16301133@bjtu.edu.cn'], subject='Test', body='哈哈，你的爬虫跑完了')


class MyImagePipeline(ImagesPipeline):  # 继承ImagesPipeline这个类

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            image_url = "http:" + image_url
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        print(results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
