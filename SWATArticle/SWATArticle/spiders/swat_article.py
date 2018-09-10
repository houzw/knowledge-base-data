# -*- coding: utf-8 -*-
import scrapy
from SWATArticle.items import SwatArticleItem


class SwatArticleSpider(scrapy.Spider):
	name = 'swat_article'
	allowed_domains = ['iastate.edu']

	def start_requests(self):
		base_url = 'https://www.card.iastate.edu/swat_articles/'
		# articles from 1984 to 2018
		end_num = 3828
		url_param = "show-details/?a="
		# 初始访问的urls
		next_urls = [base_url + url_param + str(x) for x in range(1, end_num, 1)]
		for next_url in next_urls:
			yield scrapy.Request(url=next_url, callback=self.parse)

	def parse(self, response):
		# 不要加 tbody！
		node_list = response.xpath('//table')
		for node in node_list:
			item = SwatArticleItem()
			item['title'] = node.xpath('./tr[1]/td[2]/text()').extract()
			item['authors'] = node.xpath('./tr[2]/td[2]/text()').extract()
			item['year'] = node.xpath('./tr[3]/td[2]/text()').extract()
			item['journal'] = node.xpath('./tr[4]/td[2]/text()').extract()
			item['volume'] = node.xpath('./tr[5]/td[2]/text()').extract()
			item['pages'] = node.xpath('./tr[6]/td[2]/text()').extract()
			item['doi'] = node.xpath('./tr[8]/td[2]/a/@href').extract()
			item['url'] = node.xpath('./tr[9]/td[2]/a/@href').extract()
			item['model'] = node.xpath('./tr[10]/td[2]/text()').extract()
			item['broad_application_category'] = node.xpath('./tr[11]/td[2]/text()').extract()
			item['secondary_application_category'] = node.xpath('./tr[12]/td[2]/text()').extract()
			item['watershed_description'] = node.xpath('./tr[13]/td[2]/text()').extract()
			item['calibration_summary'] = node.xpath('./tr[14]/td[2]/text()').extract()
			item['validation_summary'] = node.xpath('./tr[15]/td[2]/text()').extract()
			item['general_comments'] = node.xpath('./tr[16]/td[2]/text()').extract()
			item['abstract'] = node.xpath('./tr[17]/td[2]/text()').extract()
			item['language'] = node.xpath('./tr[18]/td[2]/text()').extract()
			item['keywords'] = node.xpath('./tr[19]/td[2]/text()').extract()
			yield item
