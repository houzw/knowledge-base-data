# -*- coding: utf-8 -*-
import scrapy


class SagaSpider(scrapy.Spider):
    name = 'saga'
    allowed_domains = ['http://saga-gis.sourceforge.net/saga_tool_doc/6.4.0/']
    start_urls = ['http://http://saga-gis.sourceforge.net/saga_tool_doc/6.4.0/index.html']

    def parse(self, response):
        pass
