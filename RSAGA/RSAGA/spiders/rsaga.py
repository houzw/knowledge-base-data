# -*- coding: utf-8 -*-
import scrapy


class RsagaSpider(scrapy.Spider):
    name = 'rsaga'
    allowed_domains = ['https://rdrr.io/cran/RSAGA/man/']
    start_urls = ['https://rdrr.io/cran/RSAGA/man/']

    def parse(self, response):
        pass
