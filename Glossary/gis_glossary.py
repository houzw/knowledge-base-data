#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/6/22 13:37

from pyquery import PyQuery as pq
import pandas as pd

url = "https://gisgeography.com/gis-dictionary-definition-glossary/"

doc = pq(url=url)
glossary_list = []
content = doc(".entry-content>p:has(strong)")
for item in content.items():
	word = item('strong').text()
	clazz = item('em').text().replace('[', '').replace(']', '')
	item('strong').remove()
	item('em').remove()
	definition = item.text().replace(':', '', 1)
	vocab = [word, clazz, definition]
	glossary_list.append(vocab)

df = pd.DataFrame(glossary_list, columns=['word', 'class', 'definition'])
writer = pd.ExcelWriter('gis_glossary.xlsx')
df.to_excel(writer)
writer.save()
