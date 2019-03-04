# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    doi = scrapy.Field()
    availability = scrapy.Field()
    provider = scrapy.Field()
    snippet = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    example = scrapy.Field()
    bands = scrapy.Field()
    terms_of_use = scrapy.Field()
    citations = scrapy.Field()
    pass
