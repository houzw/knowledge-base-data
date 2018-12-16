# -*- coding: utf-8 -*-
# @author houzhiwei
# @date 2018/7/25

import scrapy
from ..items import TaudemItem


class TaudemSpider(scrapy.Spider):
	name = 'taudem'
	allowed_domains = ['hydrology.usu.edu']
	base_url = "http://hydrology.usu.edu/taudem/taudem5/"
	start_urls = ['http://hydrology.usu.edu/taudem/taudem5/documentation.html']

	def parse(self, response):
		alist = response.xpath("//div[@class='content']/ul[5]//ul/li//a[1]")
		for a in alist:
			next_url = a.css("a::attr(href)").extract_first()
			yield scrapy.Request(self.base_url + next_url, callback=self.parse_tool)
		pass

	def parse_tool(self, resp):
		item = TaudemItem()
		item['title'] = resp.xpath("//h1[@class='gpHeading']/text()").extract_first().strip()
		# 不止一个文本节点，因此使用 //text() 并使用 extract()
		item['summary'] = resp.xpath("//div[@class='gpItemInfo'][1]//p/span//text()").extract().strip()
		item['usage'] = resp.xpath("//div[@class='gpItemInfo'][2]//p//span//text()").extract().strip()
		item['syntax'] = resp.xpath("//h2[text()='Syntax'][1]/following-sibling::div/p/text()").extract_first().strip()
		item['parameter'] = self.parse_parameter(resp)
		return item

	def parse_parameter(self, resp):
		"""提取parameter说明"""
		trs = resp.xpath("//div/table//tr[position()>1]")
		params = []
		for tr in trs:
			param = {
				"parameter": tr.xpath("./td[1]/text()").extract_first().strip(),
				"explanation": tr.xpath("./td[2]/div//span//text()").extract().strip(),
				"dataType": tr.xpath("./td[3]/text()").extract_first().strip()
			}
			if tr.xpath("./td[1][contains(text(),'Optional')]"):
				param.update({"optional": True})
			params.append(param)
		return params
