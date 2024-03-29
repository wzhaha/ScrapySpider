import scrapy
from scrapy.loader import ItemLoader
from ..items import *
import logging
import time

logger = logging.getLogger('mycustomlogger')

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        crawler.stats.set_value('hahacount', 0)
        return cls(crawler.stats)

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        for quote in response.css('div.quote'):
            time.sleep(3)
            logger.info('Parse function called on %s', response.url)
            self.stats.inc_value('hahacount')
            quoteLoader = ItemLoader(item=QuoteItem(), selector=quote)
            quoteLoader.add_css('text', 'span.text::text')
            quoteLoader.add_css('author', 'small.author::text')
            quoteLoader.add_css('tags', 'div.tags a.tag::text')

            quoteInfo = quoteLoader.load_item()

            yield quoteInfo

        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     # next_page = response.urljoin(next_page)
        #     # yield scrapy.Request(next_page, callback=self.parse)
        #     yield response.follow(next_page, callback=self.parse)


