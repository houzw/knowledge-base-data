# -*- coding: utf-8 -*-
import scrapy


class WhiteboxkbSpider(scrapy.Spider):
	name = 'whiteboxkb'
	allowed_domains = ['https://github.com/jblindsay/whitebox-tools']
	start_urls = ['https://github.com/jblindsay/whitebox-tools/']
	local_url = "file://127.0.0.1/F:/GIScience/whitebox - tools/manual/WhiteboxToolsManual.html"

	def parse(self, response):
		pass
