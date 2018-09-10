# -*- coding: utf-8 -*-
# author: houzhiwei
# https://grass.osgeo.org/grass74/manuals/r.in.aster.html

from scrapy import Spider, Request
from GrassModules.items import GrassModulesItem


class GrassSpider(Spider):
	name = 'grass'
	allowed_domains = ['grass.osgeo.org']
	start_urls = ['https://grass.osgeo.org/grass74/manuals/full_index.html']
	base_url = 'https://grass.osgeo.org/grass74/manuals/'

	def parse(self, response):
		"""处理模块命令索引页"""
		item = GrassModulesItem()
		# process requests
		trs = response.xpath("//div[@id='container']/table//tr")
		for tr in trs:
			href = tr.xpath("./td[1]/a/@href").extract_first()
			item['manual_url'] = href
			item['definition'] = tr.xpath("./td[2]/text()").extract_first()
			# meta: 将此处获取的数据传递给回调函数（callback）
			yield Request(url=self.base_url + href, meta={'item', item}, callback=self.parse_detail)

	def parse_detail(self, response):
		"""处理模块命令详情页"""
		# 接收上一层传递过来的数据
		item = response.meta['item']
		print(response.url)
		content = response.xpath("//div[@id='container']")
		item['name'] = content.xpath("./em[1]/b/text()").extract_first()
		# 第一个文本节点内容
		item['definition'] = content.xpath('./text()[1]').extract_first()
		item['keywords'] = self.parse_keywords(content)
		item['synopsis'] = self.parse_synopsis(content)
		item['flags'] = self.parse_flags(content)
		item['required_params'] = content.xpath("./div[@id='parameters']/dt[1]/text()[1]").extract_first()
		item['optional_params'] = content.xpath("./text()[1]").extract_first()
		item['description'] = content.xpath("./text()[1]").extract_first()
		item['notes'] = content.xpath("./text()[1]").extract_first()
		item['see_also'] = content.xpath("./text()[1]").extract_first()
		item['authors '] = content.xpath("./text()[1]").extract_first()
		item['source_code'] = content.xpath("./text()[1]").extract_first()
		item['examples'] = content.xpath("./text()[1]").extract_first()
		return item

	def parse_keywords(self, selector):
		"""解析命令的关键词"""
		# 文本为KEYWORDS的h2之后和文本为SYNOPSIS的h2之前的a标签
		alist = selector.xpath("./a[following::h2/text()='KEYWORDS' and preceding::h2/text()='SYNOPSIS']")
		keywords = []
		for a in alist:
			keyword = a.css('a::text').extract_first()
			keywords.append(keyword)
		return keywords

	def parse_synopsis(self, selector):
		# help = selector.xpath("./h2[text()='SYNOPSIS']/following::b[1]/text()").extract_first()
		synopsis = selector.xpath("./h2[text()='SYNOPSIS']/following::div[@id='synopsis']//text()").extract()
		return {'synopsis': synopsis}

	def parse_flags(self, selector):
		flags_dd = selector.xpath('./div[@id="flags"]/dl/dd')
		flags_dt = selector.xpath('./div[@id="flags"]/dl/dt')
		flags = []
		for i in range(1, len(flags_dt)):
			dt = flags_dt.xpath('./dt[%i]/b/text()' % i).extract_first()
			dd = flags_dd.xpath('./dd[%i]/text()' % i).extract_first()
			print(dt)
			print(dd)
			flags.append({'flag': dt, 'definition': dd})
		return flags

	def parse_required_params(self,selector):
		required = selector.xpath("./div[@id='parameters']/dl/dt/b[text()='[required]']")
		required.xpath("./[preceding-sibling::b]//text()").extract()


		return {}

	def parse_optional_params(self, selector):

		return {}

	def parse_see_also(self, selector):

		return {}





