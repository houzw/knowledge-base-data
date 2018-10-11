# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeotermsItem(scrapy.Item):
    # define the fields for your item here like:
    domain = scrapy.Field()
    term = scrapy.Field()
    term_english = scrapy.Field()
    definition = scrapy.Field()
    pass
