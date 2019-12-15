import scrapy
from ..items import *


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        author = Author()
        author['name'] = extract_with_css('h3.author-title::text')
        author['birthdate'] = extract_with_css('.author-born-date::text')
        author['bio'] = extract_with_css('.author-description::text')
        yield author


