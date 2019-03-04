# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import GdalItem
import re


# 部分命令的说明中，未说明一部分参数，例如gdalinfo中未解释 datasetname


# gdalinfo 比较特殊，需要单独处理
# gdaldem 比较特殊，需要单独处理 https://www.gdal.org/gdaldem.html
# gdaldem 有多种模式，相当于多个命令，如 gdaldem hillshade，gdaldem slope 等，每种模式参数略有差异

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
		item['name'] = resp.css('div.headertitle>div.title::text').extract_first().strip()
		item['exec'] = item['name']
		item['summary'] = resp.css('div.contents>.textblock>p:nth-child(1)::text').extract_first()
		# todo can not get content
		item['description'] = resp.xpath('//div[@class="contents"]/div[@class="textblock"]/p[preceding-sibling::h1][1]//text()').extract()
		# print(item['description'])
		#  SYNOPSIS
		item['syntax'] = resp.xpath('normalize-space(//div[@class="contents"]/div[@class="textblock"]/pre[@class="fragment"][1]/text())').extract_first()
		#  DESCRIPTION
		item['parameters'], item['options'] = self.parse_params(resp, item['syntax'])
		item['manual_url'] = resp.url
		#todo remove syntax
		example = ' '.join(resp.css('div.contents>.textblock>pre.fragment:nth-child(n+2)::text').extract()[1:])
		item['example'] = re.sub('[ ]+', ' ', example)
		# item['usage'] = resp.xpath().extract_first()
		item['comment'] = self.parse_comment(resp)
		return item

	def parse_comment(self, resp):
		comment = resp.xpath("//div[@class='contents']/div[@class='textblock']//p[preceding-sibling::dl and following-sibling::h1]//text()").extract()
		return ' '.join(comment)

	def parse_params(self, resp, syntax):
		dl = resp.xpath('//dl')
		dts = dl.xpath('.//dt')
		dds = dl.xpath('.//dd')
		# 同时遍历两个列表
		params = []
		options = []
		for dt, dd in zip(dts, dds):
			param = dict()
			flag = dt.xpath('./b/text()').extract_first()
			param['flag'] = None
			if flag:
				param['flag'] = flag.split(',')[0]
				param['name'] = param['flag'].replace('-', '')
			value = dt.xpath('./em/text()').extract_first()
			# contains "=", " ", "|" etc.
			if value:
				param['dataType'] = 'String'
				if value.strip() == 'value': param['dataType'] = 'Float'
				new_name = value.split("|")[0] if '|' in value else value.split('[')[0]
				if re.fullmatch("[a-zA-Z_0-9]+", new_name):
					param['name'] = new_name
				if ("=" or " " or "|" or '[') in value:
					param['value_format'] = value
			else:
				param['dataType'] = 'Boolean'
			if not param['flag'] and not value:
				# print(syntax)
				continue

			# d = self.parse_syntax(syntax)
			param['isOptional'] = self.is_optional(syntax, param['name'], param['flag'])
			# param['defaultValue'] = False
			param['explanation'] = ' '.join(dd.xpath('.//text()').extract())
			if len(self.required_params(syntax, param['name'])) == 1:
				param['isInputFile'] = True
				param['dataType'] = 'String'
			else:
				if ('src' or 'source' or 'filename' or 'input' or 'datasetname') in param['name']:
					param['isInputFile'] = True
					param['dataType'] = 'String'
				if ('dst' or 'dest' or 'output') in param['name']:
					param['isOutputFile'] = True
					param['dataType'] = 'String'
			if param['isOptional']:
				# choices = self.available_choices(syntax, param['flag'])
				choices = self.available_choices(self.optional_params(syntax, param['name']), param['flag'])
				if len(choices) > 0:
					param['available_choices'] = choices
				options.append(param)
			else:
				params.append(param)
		return params, options

	def is_optional(self, syntax, param_name, flag):
		if not flag: flag = param_name  # e.g. [gdal_file]*, src_dataset
		if '[' + flag in syntax:
			return True
		else:
			return False

	def available_choices(self, optional_params, flag):
		choices_list = []
		if flag:  # e.g. [gdal_file]*, src_dataset
			p = "\[" + flag + " {[a-z0-9A-Z/_|, ]+}"
			choices_match = re.search(p, optional_params)
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
		synopsis = re.sub('[\n ]+', ' ', synopsis)
		optional_params = re.search('\[[\[\]a-zA-Z0-9\- {/}<,:>=._`"*|\n]+\]', synopsis)
		optional_params = optional_params.group().replace('*', '').strip() if optional_params else ''
		return optional_params

	# io
	def required_params(self, syntax, tool_name):
		synopsis = syntax.replace('Usage: ', '').replace(tool_name, '').strip()
		synopsis = re.sub('[\n ]+', ' ', synopsis)
		required_params = re.sub('\[[\[\]a-zA-Z0-9\- {/}<,:>=._`"*|\n]+\]', '', synopsis)
		required_params = required_params.replace('*', '').strip() if required_params else ''
		return required_params
