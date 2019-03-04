# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# https://grass.osgeo.org/grass74/manuals/r.basins.fill.html

from scrapy import Item, Field


class GrassModulesItem(Item):
	name = Field()
	definition = Field()
	keywords = Field()
	# syntax
	synopsis = Field()
	parameters = Field()
	description = Field()
	notes = Field()
	see_also = Field()
	authors = Field()
	source_code = Field()
	manual_url = Field()
	pass
