# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class GdalItem(Item):
	# define the fields for your item here like:
	name = Field()
	summary = Field()
	parameters = Field()
	syntax = Field()
	manual_url = Field()
	example = Field()
	options = Field()
	description = Field()
	exec = Field()
	pass
