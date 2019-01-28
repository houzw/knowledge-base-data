# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import GdalItem
import re


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
		#  SYNOPSIS
		item['syntax'] = resp.css('div.contents>.textblock>pre.fragment:nth-child(1)::text').extract_first()
		#  DESCRIPTION
		item['parameters'], item['options'] = self.parse_params(resp, item['syntax'])
		item['manual_url'] = resp.url
		item['example'] = resp.css('div.contents>.textblock>pre.fragment:nth-child(n+2)::text').extract()
		# item['usage'] = resp.xpath().extract_first()
		return item

	def parse_params(self, resp, syntax):
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
			if name:
				param['name'] = name.replace(' ', '_')
			else:
				param['name'] = param['flag'].replace('-', '')
			# d = self.parse_syntax(syntax)
			param['isOptional'] = self.is_optional(syntax, name, param['flag'])
			param['dataType'] = 'String'
			# param['defaultValue'] = False
			param['explanation'] = dd.xpath('./dd/text()').extract_first()

			if len(self.required_params(syntax, name)) == 1:
				param['isInputFile'] = True
			else:
				if 'src' in param['name']: param['isInputFile'] = True
				if 'dst' in param['name']: param['isOutputFile'] = True

			params.append(param)
			options.append(param)
		return params, options

	def is_optional(self, syntax, tool_name, flag):
		optional_params = self.optional_params(syntax, tool_name)
		if '[' + flag in optional_params: return True
		required_params = self.required_params(syntax, tool_name)
		if flag in required_params: return False

	def available_choices(self, optional_params, flag):
		choices_list = []
		choices_match = re.search("\[" + flag + " {[a-z0-9A-Z/_|, ]+}", optional_params)
		if choices_match:
			choices = choices_match.group()
			choices = re.search('{[a-z0-9A-Z/_|, ]+}', choices).group().replace('{', '').replace('}', '').strip()
			if "," in choices:
				choices_list = choices.split(",")
			elif "/" in choices:
				choices_list = choices.split("/")
			elif "|" in choices:
				choices_list = choices.split("|")
		return choices_list

	# options
	def optional_params(self, syntax, tool_name):
		synopsis = syntax.replace('Usage: ', '').replace(tool_name, '').strip()
		optional_params = re.search('\[[\[\]a-zA-Z0-9\- <>=._`*|]+\]', synopsis)
		optional_params = optional_params.group().replace('*', '').strip() if optional_params else ''
		return optional_params

	# io
	def required_params(self, syntax, tool_name):
		synopsis = syntax.replace('Usage: ', '').replace(tool_name, '').strip()
		required_params = re.sub('\[[\[\]a-zA-Z0-9\- <>=._`*|]+\]', '', synopsis)
		required_params = required_params.replace('*', '').strip() if required_params else ''
		return required_params

# 部分命令的说明中，未说明一部分参数，例如gdalinfo中未解释 datasetname


# gdalinfo 比较特殊，需要单独处理
# gdaldem 比较特殊，需要单独处理 https://www.gdal.org/gdaldem.html
