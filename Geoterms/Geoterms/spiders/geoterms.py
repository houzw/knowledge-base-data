# -*- coding: utf-8 -*-
import scrapy
from ..items import GeotermsItem


class GeotermsSpider(scrapy.Spider):
	name = 'geoterms'
	allowed_domains = ['www.gsdkj.net:81']

	def start_requests(self):
		base_url = "http://www.gsdkj.net:81/DictView.aspx?ID="
		for i in range(1, 25524):
			print(i)
			url = base_url + str(i)
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		item = GeotermsItem()
		node = response.xpath("//form[@id='form1']//div[@class='R224']")
		item['domain'] = node.xpath("./div[@class='R2231']/text()").extract_first().replace('学科：', '')
		item['term'] = node.xpath("./div[@class='R2232']/text()").extract_first().replace('词目：', '')
		item['term_english'] = node.xpath("./div[@class='R2233']/text()").extract_first().replace('英文：', '')
		item['definition'] = node.xpath("./div[@class='R2234']/text()").extract_first().replace('释文：', '')
		yield item
