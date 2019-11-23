import scrapy
from scrapy.linkextractors import LinkExtractor


class DouBan(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250']

    # 自定义配置。自定义配置会覆盖 setting.py 中配置，即 优先级 大于 setting.py 中配置
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def parse(self, response):
        link_extractor = LinkExtractor(allow=('subject/\d+/$',), )
        links = link_extractor.extract_links(response)
        for link in links:
            print(link.url)
            yield {
                'url': link.url
            }
