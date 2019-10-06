# -*- coding: utf-8 -*-
import scrapy
from ..items import OtbItem


class OtbSpider(scrapy.Spider):
	name = 'otb'
	allowed_domains = ['www.orfeo-toolbox.org']
	start_urls = ['https://www.orfeo-toolbox.org/CookBook/Applications.html']
	base_url = 'https://www.orfeo-toolbox.org/CookBook/'

	def parse(self, response):
		alist = response.xpath("//div[contains(@class,'toctree-wrapper')]//li[@class='toctree-l2']//a")
		for a in alist:
			next_url = a.css("a::attr(href)").extract_first()
			yield scrapy.Request(self.base_url + next_url, callback=self.parse_tool)
		pass

	def parse_tool(self, resp):
		item = OtbItem()
		base_node = resp.xpath('//div[@itemprop="articleBody"]/div')
		name = base_node.xpath('./h1/text()').extract_first()
		item['name'] = name.split("-")[0].strip()
		item['manual_url'] = resp.url
		item['label'] = name.split("-")[1].strip()
		item['category'] = resp.xpath('//div[@class="rst-content"]/div[@role="navigation"]/ul/li[3]/a/text()').extract_first()
		item['definition'] = base_node.xpath('./p/text()').extract_first()
		item['authors'] = base_node.xpath('./div[@id="example"]/div[@id="authors"]/p/text()').extract_first()
		item['limitations'] = base_node.xpath('./div[@id="limitations"]/p/text()').extract_first()
		item['example'], item['command'] = self.parse_example(base_node)
		item['parameters'], item['options'] = self.parse_parameters(base_node)
		item['description'] = ' '.join(base_node.xpath('./div[@id="detailed-description"]//text()').extract()).replace('Detailed description', '').replace('¶', '')
		return item

	# normalize-space 只取第一个
	def parse_example(self, resp):
		command = resp.xpath('./div[@id="example"]/div[@class="highlight-default"][1]//span[2]/text()').extract_first()
		examples = []
		example = ' '.join(resp.xpath('./div[@id="example"]/div[@class="highlight-default"][1]//span//text()').extract())
		py_example = ' '.join(resp.xpath('./div[@id="example"]/div[@class="highlight-default"][2]//span//text()').extract())
		examples.append(example)
		examples.append(py_example)
		return examples, command

	def parse_parameters(self, resp):
		trs = resp.xpath('./div[@id="parameters"]//table[@class="docutils"]//tr')
		lis = resp.xpath('./div[@id="parameters"]//ul[@class="simple"]/li')
		# blockquote_lis = resp.xpath('./div[@id="parameters"]/blockquote/div/ul[@class="simple"]/li')
		ps = resp.xpath('./div[@id="parameters"]/p[preceding-sibling::div[@class="wy-table-responsive"]]')
		explanation = dict()
		for li in lis:
			ex = li.xpath('./text()').extract_first()
			if ex:
				ex = ex.replace(': ', '', 1)
				explanation[li.xpath('./strong/text()').extract_first()] = ex
		for p in ps:
			ex = p.xpath('./text()').extract_first()
			if ex:
				ex = ex.replace(': ', '', 1)
				explanation[p.xpath('./strong/text()').extract_first()] = ex
		params = []
		options = []
		for tr in trs[1:]:
			param = dict()
			param['flag'] = tr.xpath('./td[1]/text()').extract_first()
			param['parameterName'] = tr.xpath('./td[2]/text()').extract_first()
			param['dataType'] = tr.xpath('./td[3]//text()').extract_first()
			if param['dataType']=='Group':
				continue
			if param['dataType'] == 'Choices':
				param['availableChoices'] = []
			param['explanation'] = [value for key, value in explanation.items() if key.lower() == param['parameter_name'].lower()]
			# if 'input' in (param['parameter_name'].lower() or param['dataType'].lower()):
			if 'input' in param['dataType'].lower():
				param['isInputFile'] = True
				params.append(param)
			elif 'output' in param['dataType'].lower():
			# elif 'output' in (param['parameter_name'].lower() or param['dataType'].lower()):
				param['isOutputFile'] = True
				params.append(param)
			else:
				options.append(param)
			options = self.get_choices(options)
		return params, options

	def get_choices(self,_options):
		to_append_id = -1
		to_remove_ids = []
		for i, option in enumerate(_options):
			if option['dataType'] == 'Choices':
				to_append_id = i
			else:
				if option['dataType'] == 'Choice':
					to_remove_ids.append(i)
					choice = dict()
					choice['choice'] = option['flag'].split()[1]
					choice['description'] = option['explanation']
					_options[to_append_id]['availableChoices'].append(choice)
				else:
					to_append_id = -1
		# 倒序移除，避免移除时原列表变化导致索引超出范围
		# to_remove_ids.sort(reverse=True) # sort 会修改 to_remove_ids 并返回None！
		for i in sorted(to_remove_ids, reverse=True):
			_options.pop(i)
		return _options