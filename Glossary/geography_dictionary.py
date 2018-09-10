#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/6/22 20:52

from pyquery import PyQuery as pq
import string
from Glossary.GlossaryWriter import GlossaryWriter

base_url = "http://www.itseducation.asia/geography/"
glossary = []


def get_word(doc):
	"""获得词汇术语"""
	word = doc('p b').text()
	if not word:
		word = doc('p strong').text()
	return word


def get_definition_and_related(doc):
	doc('strong,b').remove()
	related = doc('p a[target="_blank"]').text()
	definition = doc.text().replace('-', '', 1).replace('â ', '')
	return [definition, related]


def get_ul(doc):
	ul_list = []
	uls = doc('ul')
	for ul in uls.items():
		# 获得ul之前的术语及其定义
		p_prev = ul.prevAll('p:has(span)')
		# the last one of a generator
		item = None
		for item in p_prev.items():
			pass
		ul_word = get_word(item)
		d_r = get_definition_and_related(item)
		ul_definition = d_r[0]
		ul_definition += ul.text()  # ul的内容
		ul_list.append([ul_word, ul_definition, d_r[1]])
	return ul_list


for letter in string.ascii_lowercase:
	next_url = base_url + letter + '.htm'
	# next_url = base_url + 'a.htm'
	html = pq(url=next_url)
	doc = html('div#content>table:first-of-type td:first-of-type')
	content = doc('ul,p:has(span)')
	# 先取ul的内容
	ul_list = get_ul(content)
	content('ul').remove()
	# 取其他 p 里面的内容
	for item in content.items():
		word = get_word(item)
		d_r = get_definition_and_related(item)
		vocab = [word, d_r[0], d_r[1]]
		glossary.append(vocab)
	glossary.extend(ul_list)


GlossaryWriter.write_to_excel(glossary=glossary, xlsx='geo_dict.xlsx', columns=['word', 'definition', 'seeAlso'])
