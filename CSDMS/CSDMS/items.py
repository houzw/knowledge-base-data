# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CsdmsItem(Item):
	model_name = Field()
	known_as = Field()
	model_type = Field()
	part_of = Field()  # Model part of larger framework
	incorporated = Field()  # Incorporated models or components
	dimensions = Field()  # Spatial dimensions
	extent = Field()  # Spatial extent
	domain = Field()  # Model domain
	description = Field()  # One-line model description
	extended_description = Field()  # Extended model description
	keywords = Field()  # Keywords
	# -------------------Contact---------------------
	contact = Field()
	# -------------------Technical specs---------------------
	technical = Field()
	# -------------------In/Output---------------------
	IO = Field()
	input = Field()
	output = Field()
	# -------------------Process---------------------
	process = Field()
	# -------------------Testing---------------------
	testing = Field()
	# -------------------Other---------------------
	other = Field()
	component = Field()
	publications = Field()
	pass
