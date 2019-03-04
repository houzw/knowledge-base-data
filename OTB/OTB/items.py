# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OtbItem(scrapy.Item):
    name = scrapy.Field()
    label = scrapy.Field()
    definition = scrapy.Field()
    syntax = scrapy.Field()
    command = scrapy.Field()
    parameters = scrapy.Field()
    description = scrapy.Field()
    authors = scrapy.Field()
    manual_url = scrapy.Field()
    limitations = scrapy.Field()
    example = scrapy.Field()
    options = scrapy.Field()
    category = scrapy.Field()
    pass
