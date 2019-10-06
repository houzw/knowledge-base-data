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
		item['manual_url'] = resp.url
		item['name'] = resp.xpath("//h1[@class='gpHeading']/text()").extract_first().strip()
		# 不止一个文本节点，因此使用 //text() 并使用 extract()
		item['description'] = resp.xpath("//div[@class='gpItemInfo'][1]//p/span//text()").extract()
		item['usage'] = self.get_usage(resp)
		item['syntax'] = resp.xpath("//h2[text()='Syntax'][1]/following-sibling::div/p/text()").extract_first()
		item['parameters'], item['options'] = self.parse_parameter(resp)
		return item

	def get_usage(self, resp):
		usage = resp.xpath("//div[@class='gpItemInfo'][2]//p//span//text()").extract()
		usage = [item for item in usage if item != "Command Prompt Syntax:"]
		return ' '.join(usage)

	def parse_parameter(self, resp):
		"""提取parameter说明"""
		trs = resp.xpath("//div/table//tr[position()>1]")
		params = []
		options = []
		for tr in trs:
			param = dict()
			param["parameterName"] = tr.xpath("./td[1]/text()").extract_first().strip()
			param["description"] = tr.xpath("./td[2]/div//span//text()").extract()
			param["dataType"] = tr.xpath("./td[3]/text()").extract_first().strip()
			name = str(param["parameterName"])
			if tr.xpath("./td[1][contains(text(),'Optional')]"):
				param["isOptional"] = True
			else:
				param["isOptional"] = False
			if ("Input_" in name) and ('Input_Number_of_Processes' != name):
				param['isInputFile'] = True
				param['isOutputFile'] = False
				params.append(param)
			elif "Output_" in name:
				param['isInputFile'] = False
				param['isOutputFile'] = True
				params.append(param)
			else:
				param['isInputFile'] = False
				param['isOutputFile'] = False
				param["isOptional"] = True
				options.append(param)
		return params, options
