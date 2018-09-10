#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/7/11 16:37
# https://blog.csdn.net/headwind_/article/details/70234169

from pprint import pprint
import json
from rdflib import BNode, Literal, Graph, Namespace, ConjunctiveGraph, URIRef, resource
from rdflib.namespace import SKOS, DCTERMS, RDF, RDFS, OWL

ont_uri = 'http://www.egc.org/ont/model/geospatial'
ns = Namespace(ont_uri + '#')

g = ConjunctiveGraph(identifier=ont_uri)

g.bind("skos",SKOS)
g.bind("dcterms", DCTERMS)
g.bind("model", ns)

ont_cls = ['Contact', 'TechnicalSpecs', 'InputOutput', 'Input', 'Output', 'Process', 'Testing', 'Other', 'Component',
           'Publication']
keys = ['contact', 'technical', 'io', 'input', 'output', 'process', 'testing', 'other', 'component',
        'publications']

for cls in ont_cls:
	g.add((ns[cls], RDF.type, OWL.Class))
	g.add((ns[cls], RDFS.subClassOf, OWL.Thing))

# 创建顶层类
model_cls = ns['GeoSpatialModel']
g.add((model_cls, RDF.type, OWL.Class))
g.add((model_cls, RDFS.subClassOf, OWL.Thing))

count = 0

with open('../CSDMS/csdms3.json', 'r') as f:
	data = json.load(f)  # list
# pprint(data[0]['component'])

for model_dict in data:
	# model individual
	model_name = model_dict['model_name'].replace(' ', '_')
	sub = ns[model_name]
	g.add((sub, RDF.type, model_cls))
	g.add((sub, SKOS.prefLabel, Literal(model_dict['model_name'], lang='en')))

	for k, v in model_dict.items():
		k.replace(' ', '_')
		pred = ns[k]
		if k in keys:
			i = keys.index(k)
		else:
			continue

		if type(v) == str:
			g.add((pred, RDF.type, OWL.DatatypeProperty))
			g.add((sub, pred, Literal(v)))
		elif type(v) == dict:
			v_node = BNode()
			g.add((v_node, RDF.type, ns[ont_cls[i]]))
			g.add((pred, RDF.type, OWL.ObjectProperty))
			g.add((sub, pred, v_node))
			# csdms json 最多只有两层
			for vk, vv in v.items():
				v_pred = ns[vk]
				g.add((v_pred, RDF.type, OWL.DatatypeProperty))
				g.add((v_node, v_pred, Literal(vv)))
		elif type(v) == list and len(v) > 0:
			for l in v:
				l_node = BNode()
				g.add((l_node, RDF.type, ns[ont_cls[i]]))
				g.add((sub, pred, l_node))
				for lk, lv in l.items():
					l_pred = ns[lk]
					g.add((l_pred, RDF.type, OWL.DatatypeProperty))
					g.add((l_node, l_pred, Literal(lv)))

# pprint(g.serialize(format='application/rdf+xml'))
g.serialize(destination='csdms_test.owl')
