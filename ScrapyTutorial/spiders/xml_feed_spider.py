import scrapy
from scrapy.spiders import XMLFeedSpider
class NewsSpider(XMLFeedSpider):
    name = 'news'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/rss/scroll-news.xml']
    iterator = 'itetnodes'
    itertag = 'item'

    def parse_node(self, response, node):

        item = {}
        item['title'] = node.css('title::text').get()
        item['link'] = node.css('link::text').get()
        item['desc'] = node.css('description::text').get()
        item['pub_date'] = node.css('pubDate::text').get()

        yield item