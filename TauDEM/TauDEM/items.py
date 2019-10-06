# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TaudemItem(scrapy.Item):
	name = Field()
	description = Field()
	usage = Field()
	syntax = Field()
	parameters = Field()
	options = Field()
	manual_url = Field()
	# category = Field()
	pass
