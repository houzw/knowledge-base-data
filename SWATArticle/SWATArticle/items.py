# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SwatArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # see fields https://www.card.iastate.edu/swat_articles/show-details/?a=3828
    title = scrapy.Field()
    authors = scrapy.Field()
    year = scrapy.Field()
    journal = scrapy.Field()
    volume = scrapy.Field()
    pages = scrapy.Field()
    url = scrapy.Field()
    doi = scrapy.Field()
    model = scrapy.Field()
    broad_application_category = scrapy.Field()
    primary_application_category = scrapy.Field()
    secondary_application_category = scrapy.Field()
    watershed_description = scrapy.Field()
    calibration_summary = scrapy.Field()
    validation_summary = scrapy.Field()
    general_comments = scrapy.Field()
    abstract = scrapy.Field()
    language = scrapy.Field()
    keywords = scrapy.Field()
    pass
