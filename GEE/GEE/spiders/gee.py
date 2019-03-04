# -*- coding: utf-8 -*-
import scrapy
from ..items import GeeItem

#https://developers.google.com/earth-engine/datasets/catalog/GFW_GFF_V1_fishing_hours
class GeeSpider(scrapy.Spider):
    name = 'gee'
    allowed_domains = ['developers.google.com/earth-engine/datasets/catalog/']
    start_urls = ['https://developers.google.com/earth-engine/datasets/catalog/']

    def parse(self, response):
        pass

    def parse_dataset(self,resp):
        context = resp.css("div.devsite-main-content.clearfix")
        item = GeeItem()
        item['name'] = context.css('h1.devsite-page-title[itemprop="name"]::text').extract_first()
        item['availability'] = context.css()
        pass

    def parse_bands(self,resp):
        """

        Args:
        	resp:

        Returns:

        """
        pass

    def image_properties(self,resp):
        pass