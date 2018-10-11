# -*- coding: utf-8 -*-
import scrapy
from ..items import RsagaItem

class RsagaSpider(scrapy.Spider):
    name = 'rsaga'
    allowed_domains = ['https://rdrr.io/cran/RSAGA/man/']
    start_urls = ['https://rdrr.io/cran/RSAGA/man/']

    def parse(self, response):
        pass
