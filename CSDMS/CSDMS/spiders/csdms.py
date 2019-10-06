# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Request
from CSDMS.items import CsdmsItem


class CsdmsSpider(Spider):
	name = 'csdms'
	allowed_domains = ['csdms.colorado.edu']
	base_url = 'https://csdms.colorado.edu/'
	start_urls = ['https://csdms.colorado.edu/wiki/Models_all']  # all models and tools
	# start_urls = ['https://csdms.colorado.edu/wiki/Hydrological_Models']  # Hydrological Models and tools

	def parse(self, response):
		a_list = response.css('#mw-content-text>.mw-parser-output table>tbody>tr>td:nth-child(1) a')
		for a in a_list:
			next_url = a.css('a::attr(href)').extract_first()  # page url
			name = a.css('a::text').extract_first()  # model name
			if next_url is not None:
				yield Request(self.base_url + next_url, callback=self.model_parse, meta={'name': name})

	def model_parse(self, response):
		item = CsdmsItem()
		item['model_name'] = response.meta['name']
		item = self.parse_summary(response=response, item=item)
		item = self.parse_contact(response=response, item=item)
		item = self.parse_tech(response=response, item=item)
		item = self.parse_io(response=response, item=item)
		item = self.parse_process(response=response, item=item)
		item = self.parse_testing(response=response, item=item)
		item = self.parse_other(response=response, item=item)
		item = self.parse_component(response=response, item=item)
		item = self.parse_pub(response=response, item=item)
		# yield item
		return item

	def parse_summary(self, response, item):
		"""metadata summary"""
		selector = response.xpath("//div[@id='Summary']/div")
		item['known_as'] = selector.xpath("./table[1]//tr[1]/td[2]/text()").extract_first()
		item['model_type'] = selector.xpath("./table[1]//tr[2]/td[2]/text()").extract_first()
		item['part_of'] = selector.xpath("./table[1]//tr[3]/td[2]/text()").extract_first()
		table_len = len(response.xpath("//div[@id='Summary']/div/table"))
		if table_len == 4:
			item['incorporated'] = selector.xpath("./table[2]//tr[1]/td[2]/text()").extract_first()
			item['dimensions'] = selector.xpath("./table[3]//tr[1]/td[2]/text()").extract_first()
			item['extent'] = self.split_content(selector, "./table[3]//tr[2]/td[2]/text()")
			item['domain'] = self.split_content(selector, "./table[3]//tr[3]/td[2]/text()")
			item['description'] = selector.xpath("./table[3]//tr[4]/td[2]/text()").extract_first()
			item['extended_description'] = selector.xpath("./table[3]//tr[5]/td[2]/text()").extract_first()
			item['keywords'] = ''.join(selector.xpath("./table[4]//tr[1]/td[2]//text()").extract())
		elif table_len == 3:
			item['dimensions'] = selector.xpath("./table[2]//tr[1]/td[2]/text()").extract_first()
			item['extent'] = self.split_content(selector, "./table[2]//tr[2]/td[2]/text()")
			item['domain'] = self.split_content(selector, "./table[2]//tr[3]/td[2]/text()")
			item['description'] = selector.xpath("./table[2]//tr[4]/td[2]/text()").extract_first()
			item['extended_description'] = selector.xpath("./table[2]//tr[5]/td[2]/text()").extract_first()
			item['keywords'] = ''.join(selector.xpath("./table[3]//tr[1]/td[2]//text()").extract())
		return item

	def split_content(self, selector, xpath):
		content = selector.xpath(xpath).extract_first()
		if content:
			content = content.replace('\n', '').split(',')
		content = [item.strip() for item in content]
		return content

	def parse_contact(self, response, item):
		# 取第一个
		selector = response.xpath("//div[@id='Contact']/div/table[1]")
		item['contact'] = {
			'first_name': selector.xpath(".//tr[1]/td[2]/text()").extract_first(),
			'last_name': selector.xpath(".//tr[2]/td[2]/text()").extract_first(),
			'type': selector.xpath(".//tr[3]/td[2]/text()").extract_first(),
			'institute': selector.xpath(".//tr[4]/td[2]/text()").extract_first(),
			'post_address': selector.xpath(".//tr[5]/td[2]/text()").extract_first(),
			'city': selector.xpath(".//tr[7]/td[2]/text()").extract_first(),
			'postcode': selector.xpath(".//tr[8]/td[2]/text()").extract_first(),
			'state': selector.xpath(".//tr[9]/td[2]/text()").extract_first(),
			'country': selector.xpath(".//tr[10]/td[2]/text()").extract_first(),
			'email': selector.xpath(".//tr[11]/td[2]/text()").extract_first(),
			'phone': selector.xpath(".//tr[12]/td[2]/text()").extract_first(),
			'fax': selector.xpath(".//tr[13]/td[2]/text()").extract_first(),
			}
		return item

	def parse_tech(self, response, item):
		selector = response.xpath("//div[@id='Technical_specs']/div/table")
		item['technical'] = {
			'platform': self.split_content(selector, ".//tr[1]/td[2]/text()"),
			'platform_other': selector.xpath(".//tr[2]/td[2]/text()").extract_first(),
			'program_lang': self.split_content(selector, ".//tr[3]/td[2]/text()"),
			'program_lang_other': selector.xpath(".//tr[4]/td[2]/text()").extract_first(),
			'code': self.split_content(selector, ".//tr[5]/td[2]/text()"),
			'multi_processors': selector.xpath(".//tr[6]/td[2]/text()").extract_first(),
			'dist_processors': selector.xpath(".//tr[7]/td[2]/text()").extract_first(),
			'shared_processors': selector.xpath(".//tr[8]/td[2]/text()").extract_first(),
			'start_year': selector.xpath(".//tr[9]/td[2]/text()").extract_first(),
			'in_develop': selector.xpath(".//tr[10]/td[2]/text()").extract_first(),
			'end_year': selector.xpath(".//tr[11]/td[2]/text()").extract_first(),
			'availability': selector.xpath(".//tr[12]/td[2]/text()").extract_first(),
			'source': selector.xpath(".//tr[13]/td[2]/text()").extract_first(),
			'source_web': selector.xpath(".//tr[14]/td[2]/text()").extract_first(),
			'source_csdms': selector.xpath(".//tr[15]/td[2]/text()").extract_first(),
			'license': selector.xpath(".//tr[16]/td[2]/text()").extract_first(),
			'license_other': selector.xpath(".//tr[17]/td[2]/text()").extract_first(),
			'memory': selector.xpath(".//tr[18]/td[2]/text()").extract_first(),
			'run_time': selector.xpath(".//tr[19]/td[2]/text()").extract_first(),
			}
		return item

	def parse_io(self, response, item):
		selector = response.xpath("//div[@id='In_2FOutput']/div/table")
		item['input'] = {
			'params': ''.join(selector.xpath(".//tr[1]/td[2]//text()").extract()),
			'format': self.split_content(selector, ".//tr[2]/td[2]/text()"),
			'format_other': selector.xpath(".//tr[3]/td[2]/text()").extract_first()
			}
		item['output'] = {
			'params': ''.join(selector.xpath(".//tr[4]/td[2]//text()").extract()),
			'format': self.split_content(selector, ".//tr[5]/td[2]/text()"),
			'format_other': selector.xpath(".//tr[6]/td[2]/text()").extract_first()
			}
		item['IO'] = {
			'pre_soft_need': selector.xpath(".//tr[7]/td[2]/text()").extract_first(),
			'pre_soft_description': selector.xpath(".//tr[8]/td[2]/text()").extract_first(),
			'post_soft_need': selector.xpath(".//tr[9]/td[2]/text()").extract_first(),
			'post_soft_description': selector.xpath(".//tr[10]/td[2]/text()").extract_first(),
			'visual_soft_need': selector.xpath(".//tr[11]/td[2]/text()").extract_first(),
			'visual_soft': selector.xpath(".//tr[12]/td[2]/text()").extract_first(),
			'visual_soft_other': selector.xpath(".//tr[13]/td[2]/text()").extract_first()
			}
		return item

	def parse_process(self, response, item):
		selector = response.xpath("//div[@id='Process']/div/table")
		item['process'] = {
			'processes': ' '.join(selector.xpath(".//tr[1]/td[2]//text()").extract()),
			'params_equations': ' '.join(selector.xpath(".//tr[2]/td[2]//text()").extract()),
			'length_scale_resolution': selector.xpath(".//tr[3]/td[2]/text()").extract_first(),
			'time_scale_resolution': selector.xpath(".//tr[4]/td[2]/text()").extract_first(),
			'limits': selector.xpath(".//tr[5]/td[2]/text()").extract_first()
			}
		return item

	def parse_testing(self, response, item):
		selector = response.xpath("//div[@id='Testing']/div/table")
		item['testing'] = {
			'calibration_data_description': selector.xpath(".//tr[1]/td[2]/text()").extract_first(),
			'calibration_data': selector.xpath(".//tr[2]/td[2]/text()").extract_first(),
			'data_description': selector.xpath(".//tr[3]/td[2]/text()").extract_first(),
			'test_data': selector.xpath(".//tr[4]/td[2]/text()").extract_first(),
			'ideal_test_data': selector.xpath(".//tr[5]/td[2]/text()").extract_first(),
			}
		return item

	def parse_other(self, response, item):
		selector = response.xpath("//div[@id='Other']/div")
		item['other'] = {
			'collaborating': selector.xpath("./table[1]//tr[1]/td[2]/text()").extract_first(),
			'manual_available': selector.xpath("./table[2]//tr[1]/td[2]/text()").extract_first(),
			'manual': selector.xpath("./table[2]//tr[2]/td[2]/text()").extract_first(),
			'model_web': ''.join(selector.xpath("./table[2]//tr[3]/td[2]//text()").extract()),
			'forum': selector.xpath("./table[2]//tr[4]/td[2]/text()").extract_first(),
			'comments': selector.xpath("./table[3]//tr[1]/td[2]/text()").extract_first(),
			}
		return item

	def parse_component(self, response, item):
		selector = response.xpath("//div[@id='Component_info']/div")
		item['component'] = {
			'openmi': selector.xpath("./table[1]//tr[1]/td[2]/text()").extract_first(),
			'bmi': selector.xpath("./table[1]//tr[2]/td[2]/text()").extract_first(),
			'wmt': selector.xpath("./table[1]//tr[3]/td[2]/text()").extract_first(),
			'model_doi': selector.xpath("./table[2]//tr[1]/td[2]/text()").extract_first(),
			'model_version': selector.xpath("./table[2]//tr[2]/td[2]/text()").extract_first(),
			'year_version': selector.xpath("./table[2]//tr[3]/td[2]/text()").extract_first(),
			'file_link': selector.xpath("./table[2]//tr[4]/td[2]/text()").extract_first(),
			'couple_with': selector.xpath("./table[3]//tr[1]/td[2]/text()").extract_first(),
			}
		return item

	def parse_pub(self, response, item):
		trs = response.css("table.sortable tbody tr")
		pubs = []
		for tr in trs:
			title = tr.xpath("./td[1]/text()").extract_first()
			if not title:
				continue
			year = tr.xpath("./td[2]/text()").extract_first()
			model = ' '.join(tr.xpath("./td[3]//text()").extract())
			ref_type = tr.xpath("./td[4]/text()").extract_first()
			pubs.append({'title': title, 'year': year, 'model': model, 'ref_type': ref_type})
		item['publications'] = pubs
		return item
