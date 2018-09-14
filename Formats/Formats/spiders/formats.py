# -*- coding: utf-8 -*-
import scrapy


class FormatsSpider(scrapy.Spider):
    """GIS 数据格式"""
    name = 'formats'
    allowed_domains = ['http://www.bluemarblegeo.com/products/global-mapper-formats.php']
    start_urls = ['http://www.bluemarblegeo.com/products/global-mapper-formats.php/']

    def parse(self, response):
        pass
