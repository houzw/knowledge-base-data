#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/9/10 18:58
from owlready2 import *
import json

model_uri = 'http://www.egc.org/ont/process/taudem'
# create and import ontologies
skos_file = 'file://skos.rdf'
dcterms_file = 'file://dcterms.rdf'
onto = get_ontology(model_uri)
skos = get_ontology(skos_file).load()
dcterms = get_ontology(dcterms_file).load()
onto.imported_ontologies.append(skos)
onto.imported_ontologies.append(dcterms)

with onto:
	class TauDEMTool(Thing):
		pass


	class Parameter(Thing):
		pass


def create_onto_class(name, parent_class):
	with onto:
		clazz = types.new_class(name, (parent_class,))
	return clazz


with open('../TauDEM/taudem.json', 'r') as f:
	data = json.load(f)  # list

for d in data:
	# 实例
	tool_name = d['title'].strip().replace(' ', '_')
	tool = TauDEMTool(tool_name, prefLabel=locstr(d['title'], lang='en'))
	for k, v in d.items():
		if k == 'parameter' and type(v) == list:
			for item in v:
				param = Parameter()
				k_name = 'has' + k.capitalize() + 'Object'
				create_onto_class(k_name, ObjectProperty)
				tool.__getattr__(k_name).append(param)
				for itemK, itemV in item.items():
					itemK_name = 'has' + itemK.capitalize()
					create_onto_class(itemK_name, DataProperty)
					if type(itemV) == list:
						param.__getattr__(itemK_name).append(''.join(itemV))
					else:
						param.__getattr__(itemK_name).append(itemV)
		else:
			k_name = 'has' + k.capitalize()
			create_onto_class(k_name, DataProperty)
			if not v:
				continue
			if type(v) == list:
				if len(v) > 0:
					tool.__getattr__(k_name).append(''.join(v))
			else:
				tool.__getattr__(k_name).append(v)

onto.save(file='taudem.owl', format="rdfxml")

