# -*- coding: utf-8 -*-
import scrapy
from ..items import SagaItem


class SagaSpider(scrapy.Spider):
	name = 'saga'
	allowed_domains = ['saga-gis.org']
	start_urls = ['http://www.saga-gis.org/saga_tool_doc/7.0.0/a2z.html']
	base_url = 'http://www.saga-gis.org/saga_tool_doc/7.0.0/'

	def parse(self, response):
		alist = response.xpath('//table//tr[position()>1]/td[1]/a')
		print('alist')
		print(alist)
		for a in alist:
			next_url = a.css("a::attr(href)").extract_first()
			print(next_url)
			yield scrapy.Request(self.base_url + next_url, callback=self.parse_content)

	def parse_content(self, resp):
		item = SagaItem()
		item['name'] = resp.xpath("//main/h1/text()").extract_first()
		item['comment'] = resp.xpath("//main/p//text()").extract()
		item['command'] = resp.xpath("//main/pre[@class='usage']//text()").extract()
		item['parameter'] = self.parse_parameters(resp.xpath("//main/table"))
		return item

	@staticmethod
	def parse_parameters(table):
		trs = table.xpath("//tr[position()>1]")
		input_trs = []
		output_trs = []
		options_trs = []
		in_rows = 0
		out_rows = 0
		for tr in trs:
			if tr.xpath("./td[1][contains(text(),'Input')]"):
				in_rows = int(tr.xpath("./td[1][contains(text(),'Input')]/@rowspan").extract_first().strip())
				input_trs.append(trs[:in_rows])
			elif tr.xpath("./td[1][contains(text(),'Output')]"):
				out_rows = int(tr.xpath("./td[1][contains(text(),'Output')]/@rowspan").extract_first().strip())
				output_trs.append(trs[in_rows:in_rows + out_rows])
			else:
				options_trs.append(trs[in_rows + out_rows:])

		inputs = []
		for tr in input_trs:
			i = 0
			if tr.xpath("./td[1][@class='labelSection']"):
				i = 1
			input_param = {
				"name": tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first(),
				"type": tr.xpath("./td[" + str(i + 2) + "]/text()").extract_first(),
				"identifier": tr.xpath("./td[" + str(i + 3) + "]//text()").extract_first(),
				"description": tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first(),
				"constraints": tr.xpath("./td[" + str(i + 5) + "]//text()").extract()
			}
			inputs.append(input_param)

		outputs = []
		for tr in output_trs:
			i = 0
			if tr.xpath("./td[1][@class='labelSection']"):
				i = 1
			output = {
				"name": tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first(),
				"type": tr.xpath("./td[" + str(i + 2) + "]/text()").extract_first(),
				"identifier": tr.xpath("./td[" + str(i + 3) + "]/text()").extract_first(),
				"description": tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first(),
				"constraints": tr.xpath("./td[" + str(i + 5) + "]//text()").extract()
			}
			outputs.append(output)

		options = []
		for tr in options_trs:
			i = 0
			if tr.xpath("./td[1][@class='labelSection']"):
				i = 1
			option = {
				"name": tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first(),
				"type": tr.xpath("./td[" + str(i + 2) + "]/text()").extract_first(),
				"identifier": tr.xpath("./td[" + str(i + 3) + "]/text()").extract_first(),
				"description": tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first(),
				"constraints": tr.xpath("./td[" + str(i + 5) + "]//text()").extract()
			}
			options.append(option)

		parameter = {
			"input": inputs,
			"output": outputs,
			"options": options
		}
		return parameter
