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
# https://github.com/OSGeo/gdal-docs
# file:///H:/gisdemo/gdal-docs/programs/gdalinfo.html

class GdalSpiderSpider(scrapy.Spider):
	name = 'gdal_spider'
	# start_urls = ['file://127.0.0.1/H:/gisdemo/gdal-docs/programs/index.html']
	start_urls = ['https://gdal.org/programs/index.html']
	base_url = 'https://gdal.org/programs/'

	def parse(self, response):
		a_list = response.css('div#programs ul>li a.reference.internal')
		for a in a_list:
			next_url = a.css('a::attr(href)').extract_first()
			if next_url.endswith('common-options'):
				continue
			yield Request(self.base_url + next_url, callback=self.parse_content)

	def parse_content(self, resp):
		item = GdalItem()
		content = resp.css('div[itemprop="articleBody"]>div.section')
		item['name'] = content.css('h1:nth-child(2)::text').extract_first().strip()
		item['exec'] = item['name']  # description > p:nth-child(2)#description > p:nth-child(3)
		item['summary'] = content.css('p:nth-child(3)::text').extract_first()
		# first two p
		description = ' '.join(resp.xpath('.//div[@id="description"]/p[preceding-sibling::h2[contains(text(),"Description")] and following-sibling::dl]//text()').extract())
		desc_append = '\n'.join(content.css('#description>ul.simple>li>p::text').extract())
		# print(description)
		if not description:
			print(description)
		if not desc_append:
			item['description'] = description
		else:
			item['description'] = description + desc_append
		# print(item['description'])
		#  SYNOPSIS
		item['syntax'] = self.parse_synopsis(content)
		item['parameters'], item['options'] = self.parse_params(resp)
		item['manual_url'] = resp.url
		item['example'] = self.parse_example(content)
		return item

	def parse_synopsis(self, content):
		synopsis = ' '.join(content.css('#synopsis .highlight-default.notranslate pre>span::text').extract())
		synopsis = synopsis.replace('Usage :', '')
		synopsis = synopsis.replace('[ ', '[').replace(' ]', ']') \
			.replace('< ', '').replace(' >', '') \
			.replace('- ', '-').replace(' = ', '=') \
			.replace(' . ', '.').strip()
		return synopsis

	def parse_example(self, content):
		example = ' '.join(content.css('#example>.highlight-default.notranslate>.highlight>pre>span::text').extract()[1:])
		example = example.replace('- ', '-').replace(' = ', '=').replace(' . ', '.').strip()
		return example

	def parse_params(self, resp):
		dls = resp.css('#description dl.option')
		params = []
		options = []
		for dl in dls:
			param = dict()
			flag_value = None
			param_name = None
			if len(dl.css("dt>code.descname")) > 1:
				param['flag'] = dl.css("dt>code.descname:nth-child(1)::text").extract_first()
				param['long_flag'] = dl.css("dt>code.descname:nth-child(4)::text").extract_first()
				flag_value = dl.css("dt>code.descclassname:nth-child(5)::text").extract_first()
			else:
				# e.g. -b <band>
				param['flag'] = dl.css("dt>code.descname::text").extract_first()
				flag_value = dl.css("dt>code.descclassname::text").extract_first()
			param['dataType'] = 'String'
			if flag_value is None:
				param_name = param['flag']
				param['dataType'] = 'Boolean'
				param['isOptional'] = True
			else:
				# default is not optional, reset to true if required
				param['isOptional'] = False
				if param_name is None:
					param_name = flag_value.replace('=', '')
					if flag_value == '<n>':
						param_name = param['flag']
				spliters = [' ', '|', ',', '=']
				if any([spliter in flag_value.strip() for spliter in spliters]):
					param_name = param['flag']
					if flag_value.startswith('='):
						flag_value = flag_value.replace('=', '')
					param['input_pattern'] = flag_value.strip()
				elif flag_value.strip() == 'value':
					param['dataType'] = 'Float'
				param = self.handle_avaliables(param, flag_value)

			if 'long_flag' in param.keys() and param['long_flag']:
				param_name = param['long_flag']

			if flag_value:
				if flag_value.strip().startswith('<') or flag_value.strip().startswith('[') or flag_value.strip().startswith('{'):
					param['isOptional'] = True

			if param['flag'] in ['-h', '-v', '-q', '--version', '-c']:
				param['isOptional'] = True
			if param['flag'].startswith('<'):
				param['flag'] = re.sub('[<>]', '', param['flag'].strip())
				param['isOptional'] = True
			param['name'] = re.sub('[<>:\-=\[\]]+', '', param_name.strip()).replace(' ', '_').lower()
			if ('src' or 'source' or 'filename' or 'input' or 'datasetname') in param['name']:
				param['isInputFile'] = True
				param['dataType'] = 'String'
			if ('dst' or 'dest' or 'output') in param['name']:
				param['isOutputFile'] = True
				param['dataType'] = 'String'
			param['explanation'] = ' '.join(dl.css("dd *::text").extract())
			if param['isOptional']:
				options.append(param)
			else:
				params.append(param)

		return params, options

	def handle_avaliables(self, param, flag_value):
		# -expand gray|rgb|rgba
		# -outsize <xsize>[%]|0 <ysize>[%]|0
		# -tr <xres> <yres>
		available_values = None
		flag_value = flag_value.strip()
		if '|' in flag_value:
			available_values = flag_value.split("|")
		elif ',' in flag_value:
			flag_value = flag_value.replace('{', '').replace('}', '')
			available_values = flag_value.split(",")
		elif '/' in flag_value:
			available_values = flag_value.split("/")
		if available_values:
			param['available_values'] = [re.sub("[<>\[{}]+", '', available_value.strip()) for available_value in available_values]
		else:
			param['available_values'] = available_values
		return param
