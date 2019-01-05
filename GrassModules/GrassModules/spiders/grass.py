# -*- coding: utf-8 -*-
# author: houzhiwei
# https://grass.osgeo.org/grass74/manuals/r.fill.stats.html

from scrapy import Spider, Request
from GrassModules.items import GrassModulesItem
import re

class GrassSpider(Spider):
	name = 'grass'
	# allowed_domains = ['grass.osgeo.org']
	# start_urls = ['https://grass.osgeo.org/grass74/manuals/full_index.html']
	# base_url = 'https://grass.osgeo.org/grass74/manuals/'

	start_urls = ['file://127.0.0.1/H:/gisdemo/grass-7.5_html_manual/manuals/full_index.html']
	base_url = 'file://127.0.0.1/H:/gisdemo/grass-7.5_html_manual/manuals/'

	def parse(self, response):
		"""处理模块命令索引页"""
		# process requests
		tables = response.xpath("//div[@id='container']//table")
		# print(tables)
		for table in tables:
			trs = table.xpath("//tr")
			for i, tr in enumerate(trs):
				# if i > 1:
				# 	return
				href = tr.xpath("./td[1]/a/@href").extract_first()
				# meta: 将此处获取的数据传递给回调函数（callback）
				yield Request(url=self.base_url + href, callback=self.parse_detail)

	def parse_detail(self, response):
		"""处理模块命令详情页"""
		item = GrassModulesItem()
		item['manual_url'] = response.url.replace('file://127.0.0.1/H:/gisdemo/grass-7.5_html_manual/manuals/',"https://grass.osgeo.org/grass77/manuals/")
		content = response.css("#container")
		item['name'] = content.css("#name>b::text").extract_first()
		# print('name %s' % item['name'])
		item['definition'] = content.xpath('normalize-space(./h2[1][contains(text(),"NAME")]/following-sibling::text()[2])').extract_first()
		item['keywords'] = self.parse_keywords(content)
		item['synopsis'] = self.parse_synopsis(content)
		item['parameters'] = self.parse_params(content)
		item['description'] = self.parse_des(content)
		item['notes'] = self.parse_notes(content)
		item['see_also'] = self.parse_see_also(content)
		item['authors'] = self.parse_authors(content)
		item['source_code'] = self.parse_source(content)
		return item

	def parse_keywords(self, selector):
		"""解析命令的关键词"""
		# 文本为KEYWORDS的h2之后和文本为SYNOPSIS的h2之前的a标签?
		a_path = './a[preceding-sibling::h2[contains(text(),"KEYWORDS")] and following-sibling::h2[contains(text(),"SYNOPSIS")]]'
		keywords_list = selector.xpath(a_path)
		keywords = []
		for keyword in keywords_list:
			word = keyword.xpath('normalize-space(.//text())').extract_first()
			keywords.append(word)
		# print('keywords %s' % keywords)
		return keywords

	def parse_synopsis(self, selector):
		# help = selector.xpath("./h2[text()='SYNOPSIS']/following::b[1]/text()").extract_first()
		synopsis = selector.css("#synopsis *::text").extract()
		# print('synopsis: %s' % ''.join(synopsis))
		return ''.join(synopsis).strip()

	def parse_flags(self, selector):
		"""解析flags，当做parameters"""
		dl = selector.xpath('./div[@id="flags"]/dl')
		flags_dt = dl.xpath('.//dt')
		flags = []
		for i in range(0, len(flags_dt)):
			flag = flags_dt[i].xpath('./b/text()').extract_first()
			# print('flag %s' % dt)
			dds = flags_dt[i].xpath('./following-sibling::dd[following-sibling::dt[1]]')
			flag_exp = dds.xpath('.//text()').extract()
			flags.append(
				{'parameter': str(flag).replace("-", ""), 'flag': flag, 'explanation': ' '.join(flag_exp),
				 'optional': True, })
		return flags

	def parse_params(self, selector):
		parameters = self.parse_flags(selector)
		dts = selector.css("#parameters>dl>dt")
		for i in range(0, len(dts)):
			parameter = dict()
			data_type = 'String'
			input_file = False
			out_file = False
			optional = True
			dt = dts[i]
			# key
			dt_id = dt.xpath('./b[1]/text()').extract_first().strip()
			parameter['parameter'] = dt_id
			parameter['flag'] = dt_id
			if dt_id == 'input':
				input_file = True
			elif dt_id == 'output':
				out_file = True
			# value
			param_type = dt.xpath('string(./em//text())').extract()
			if param_type == 'name':
				data_type = 'String'
			elif param_type == 'name[,name,...]':
				data_type = 'List'
			elif param_type == 'value':
				data_type = 'Double'
			elif param_type == 'character':
				data_type = 'String'
			elif param_type == 'float':
				data_type = 'Float'
			parameter['dataType'] = data_type
			# required
			require = dt.xpath('./b[2]/text()').extract_first()
			if require == '[required]':
				optional = False
			parameter['optional'] = optional
			# 后面的所有非空节点
			dds_test = dt.xpath('./following-sibling::node()[not(string-length(text())=0)]')
			dd_list = []
			# 遍历所有节点，直到遇到 dt
			for i, item in enumerate(dds_test):
				if len(item.css('dt')) > 0:
					break
				dd_list.append(item)
			# print("dd_list %s" % dd_list)
			# dds = dt.xpath('./following-sibling::dd[following-sibling::dt[1] or not(following-sibling::dt)]')
			# print("dds %s" % dds)
			(explanation, alternatives, default) = self.parse_explanation(dd_list)
			parameter['explanation'] = explanation
			parameter['defaultValue'] = default
			parameter['alternatives'] = alternatives
			if re.search('Name of input', explanation) is not None:
				input_file = True
			if re.search('Name for output',explanation) is not None:
				out_file = True
			parameter['isInputFile'] = input_file
			parameter['isOutputFile'] = out_file
			# parameter['supportFormats'] = ''
			parameters.append(parameter)
		# print("parameters %s" % parameters)
		return parameters

	def parse_explanation(self, dd_list):
		"""explanation"""
		explanation = None
		alternatives = None
		default = None
		# length = len(dd_list)
		for j, item in enumerate(dd_list):
			if j == 0 and item:
				explanation = item.css('dd::text').extract_first().strip()
				# print("explanation %s" % explanation)
				continue
			if alternatives is None:
				# 若alternatives已经有值了，则不再处理
				alternatives = item.xpath('./em[parent::dd[contains(normalize-space(text()),"Options:")]][1]/text()').extract_first()
				if alternatives is not None:
					# print("alternatives %s" % alternatives)
					alternatives = str(alternatives).replace('Options:', '')
					continue
				else:
					alternatives = item.xpath(
						'./text()[parent::dd[contains(normalize-space(text()),"Special characters:")]]').extract_first()
					if alternatives is not None:
						alternatives = str(alternatives).replace('Special characters:', '')
						# print("alternatives %s" % alternatives)
						continue
			if default is None:
				default = item.xpath('./em[parent::dd[contains(normalize-space(text()),"Default:")]][1]/text()').extract_first()
				if not default:
					continue
				# print("default %s" % default)
		# 整理格式
		if alternatives is not None:
			alternatives = alternatives.split(',')
			alternatives = [x.strip() for x in alternatives]
		# if default is not None:
		# 	default = default.split(',')
		# 	default = [x.strip() for x in default]
		return explanation, alternatives, default

	def parse_des(self, selector):
		desc_selector = selector.xpath(".//a[@name='description']/parent::h2")
		em = desc_selector.xpath("normalize-space(./following-sibling::em/text())").extract_first()
		# print('em %s' % em)
		des = desc_selector.xpath(
			"normalize-space(./following-sibling::em/following-sibling::text()[1])").extract_first()
		# print('des %s' % des)
		return str(em) + str(des)

	def parse_notes(self, selector):
		notes = selector.xpath(
			"normalize-space(.//text()[preceding-sibling::h2[child::a[@name='notes']] and following-sibling::h2[child::a[@name='see-also']]])").extract()
		# print('notes %s' % notes)
		return ''.join(notes)

	def parse_see_also(self, selector):
		also_selector = selector.xpath(".//a[@name='see-also']/parent::h2")
		alist = also_selector.xpath("./following-sibling::em//a")
		alsos = []
		for a in alist:
			also = a.xpath("normalize-space(.//text())").extract_first()
			alsos.append(also)
		# print('alsos %s' % alsos)
		return alsos

	def parse_authors(self, selector):
		authors_selector = selector.xpath(".//a[@name='authors' or @name='author']/parent::h2")
		authors = authors_selector.xpath("normalize-space(./following-sibling::text()[position()<3])").extract()
		# print('authors %s' % authors)
		return authors

	def parse_source(self, selector):
		source = selector.xpath(
			"./h2[contains(text(),'SOURCE CODE')]/following-sibling::p/a/@href").extract_first()
		return source
