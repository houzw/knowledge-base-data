# -*- coding: utf-8 -*-
import scrapy

# https://www.gdal.org/index.html
class GdalSpiderSpider(scrapy.Spider):
    name = 'gdal_spider'
    allowed_domains = ['gdal.org']
    start_urls = ['http://www.gdal.org/']

    def parse(self, response):
        pass
