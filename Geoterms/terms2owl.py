#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/24 16:34


from owlready2 import *
import json
from os import path
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
import datetime

model_uri = 'http://www.egc.org/ont/vocab/geo'
onto = get_ontology(model_uri)

onto_path.append(path.normpath(path.dirname(__file__)) + '/')
skos = get_ontology('file://../JSON2OWL/OwlConvert/skos.rdf').load(only_local=True)
dcterms = get_ontology('file://../JSON2OWL/OwlConvert/dcterms.rdf').load(only_local=True)
onto.imported_ontologies.append(skos)
onto.imported_ontologies.append(dcterms)
onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('Geographic Terms')
onto.metadata.source.append('http://www.gsdkj.net:81/DictView.aspx')
onto.metadata.created.append(datetime.datetime.today())
print('ontologies imported')
# OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
with onto:
	class GeoTerms(Thing):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/term.json', 'r', encoding='utf-8') as f:
	jdata = json.load(f)  # list


for d in jdata:
	domain = d['domain']
	if not onto[domain]: OWLUtils.create_onto_class(onto, domain, GeoTerms)
	term = d['term']
	term_english = d['term_english']
	definition_cn = d['definition']
	if onto[term] and (GeoTerms in onto[term].is_a):
		# 不能用definition？
		onto[domain].definition.append(definition_cn)
	else:
		indi = onto[domain](term, prefLabel=locstr(term_english, lang='en'), altLabel=locstr(term, lang='zh-CN'))
		print(onto[domain])
		print(indi)
		indi.definition.append(definition_cn)

# onto.save("geoterms.owl", format="rdfxml")
# print("terms DONE!")
