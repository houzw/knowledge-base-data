#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/7/19 18:21
"""
注意在转换之前去掉一些Json中的 \u200e
"""

from owlready2 import *
import types
import json

model_uri = 'http://www.egc.org/ont/model/hydrology'
# create and import ontologies
skos_file = 'file://skos.rdf'
dcterms_file = 'file://dcterms.rdf'
csdms_base_file = 'file://csdms.owl'
onto = get_ontology(model_uri)
skos = get_ontology(skos_file).load()
dcterms = get_ontology(dcterms_file).load()
csdms = get_ontology(csdms_base_file).load()
onto.imported_ontologies.append(skos)
onto.imported_ontologies.append(dcterms)
onto.imported_ontologies.append(csdms)

# 基本的类及属性都已经定义在csdms.owl文件中了

ont_cls = ['Contact', 'TechnicalSpecs', 'InputOutput', 'Input', 'Output', 'Process', 'Testing', 'Other',
           'Component', 'Publication']
keys = ['contact', 'technical', 'IO', 'input', 'output', 'process', 'testing', 'other', 'component',
        'publications']

with open('../CSDMS/hydro.json', 'r', encoding='utf8') as f:
	data = json.load(f)  # list

for model_dict in data:
	# model individual
	model_name = model_dict['model_name'].strip().replace(' ', '_')
	domains = model_dict['domain'].split(',')
	clazzs = []
	# 模型类型
	for domain in domains:
		domain = domain.strip().replace(' ', '_')
		if model_dict['model_type'] == 'Tool':
			clazzs.append(csdms[domain + "Tool"])
		else:
			clazzs.append(csdms[domain + "Model"])
	# 实例, 属于多个类
	model = clazzs[0](model_name, prefLabel=locstr(model_name, lang='en'), namespace=onto)
	for i, clazz in enumerate(clazzs):
		if i > 0:
			model.is_a.append(clazz)

	for k, v in model_dict.items():
		k_name = k.replace(' ', '_')  # e.g. known_as
		k_name = "has" + k_name.capitalize()
		# 判断是否应该创建 blank node
		if k == "model_name":
			continue
		if k == "description":
			model.description.append(v)
			continue
		if k == "known_as":
			model.altLabel.append(v)
			continue
		if k in keys:
			i = keys.index(k)

		# 基本信息
		if type(v) == str:
			# 创建属性类
			# 给实例添加属性。此处属性为动态获得，因此无法直接使用点（.）方法进行调用
			model.__getattr__(k_name).append(v)
		# 复合信息
		elif type(v) == dict:
			b_node = csdms[ont_cls[i]](namespace=onto)  # blank node
			model.__getattr__(k_name).append(b_node)  # relation
			# csdms json 最多只有两层
			for vk, vv in v.items():
				pred1 = "has" + vk.capitalize()
				if vv is not None:
					b_node.__getattr__(pred1).append(vv)
		elif type(v) == list and len(v) > 0:
			for l in v:
				l_node = csdms[ont_cls[i]](namespace=onto)
				model.__getattr__(k_name).append(l_node)
				for lk, lv in l.items():
					pred2 = "has" + lk.capitalize()
					if lv is not None:
						l_node.__getattr__(pred2).append(lv)

# save to file
onto.save(file='hydromodel.owl', format="rdfxml")
