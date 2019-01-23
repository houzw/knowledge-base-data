# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import GdalItem


# https://www.gdal.org/index.html
class GdalSpiderSpider(scrapy.Spider):
	name = 'gdal_spider'
	allowed_domains = ['gdal.org']
	start_urls = ['https://www.gdal.org/gdal_utilities.html', 'https://www.gdal.org/ogr_utilities.html', 'https://www.gdal.org/gnm_utilities.html']
	base_url = 'https://www.gdal.org/'

	def parse(self, response):
		a_list = response.css('div.contents ul>li>a')
		for a in a_list:
			next_url = a.css('a::attr(href)').extract_first()
			yield Request(self.base_url + next_url, callback=self.parse_content)

	def parse_content(self, resp):
		item = GdalItem()
		item['name'] = resp.css('div.headertitle>div.title::text').extract_first()
		item['exec'] = item['name']
		item['summary'] = resp.css('div.contents>.textblock>p:nth-child(1)::text').extract_first()
		item['description'] = resp.css('div.contents>.textblock>p:nth-child(2)::text').extract_first()
		print(item['description'])
		item['syntax'] = resp.css('div.contents>.textblock>pre.fragment:nth-child(1)::text').extract_first()
		item['parameters'], item['options'] = self.parse_params(item['syntax'], resp)
		item['manual_url'] = resp.url
		item['example'] = resp.css('div.contents>.textblock>pre.fragment:nth-child(n+2)::text').extract()
		# item['usage'] = resp.xpath().extract_first()
		return item

	def parse_params(self, syntax, resp):
		d = self.parse_syntax(syntax)
		dl = resp.xpath('//dl')
		dts = dl.xpath('.//dt')
		dds = dl.xpath('.//dd')
		# 同时遍历两个列表
		params = []
		options = []
		for dt, dd in zip(dts, dds):
			print(dt, dd)
			param = dict()
			name = dt.xpath('./dt/em/text()').extract_first()
			param['flag'] = dt.xpath('./dt/b/text()').extract_first()
			if id:
				param['name'] = name.replace(' ', '_')
			elif param['flag']:
				param['name'] = param['flag'].replace('-', '')
			param['isOptional'] = True
			param['defaultValue'] = False
			param['explanation'] = dd.xpath('./dd/text()').extract_first()
			param['isInputFile'] = False
			param['isOutputFile'] = False
			params.append(param)
			options.append(param)
		return params, options

	def parse_syntax(self, syntax):
		return dict()

# gdalinfo 比较特殊，需要单独处理
