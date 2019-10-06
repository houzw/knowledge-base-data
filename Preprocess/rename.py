#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/3/21 16:10

from owlready2 import *
from os import path


"""
rename localname of ontology classes and individuals to uuid 
"""
onto_path.append(path.normpath(path.dirname(__file__)) + '/')
skos = get_ontology('/skos.rdf').load(only_local=True)
dc = get_ontology('/dcterms.rdf').load(only_local=True)
UniProps = get_ontology('/UniProps.owl').load(only_local=True)
hydrology = get_ontology('/hydrology.owl').load(only_local=True)
csdms = get_ontology('/csdms-standard-names.owl').load(only_local=True)


# def rename(obj_list):
# 	for o in obj_list:
# 		uid = uuid.uuid1()
# 		label = o.prefLabel
# 		name = str(o.name).replace('_', ' ')
# 		if not label or label[0] == '':
# 			o.prefLabel = name
# 		elif name != label:
# 			o.hiddenLabel = name
# 		o.name = uid
# 		print(o.prefLabel)

graph = default_world.as_rdflib_graph()



def name_to_label(_onto):
	_classes = _onto.classes()
	for _class in _classes:
		name = _class.name.replace('_', ' ')
		_class.prefLabel = locstr(name, lang='en')
		_instances = _class.instances()
		for _instance in _instances:
			ins_name = _instance.name.replace('_', ' ')
			_instance.prefLabel = locstr(ins_name, lang='en')


def remove_label_underline(_onto):
	_classes = _onto.classes()
	for cls in _classes:
		if cls.prefLabel:
			cls_label = cls.prefLabel[0].replace('_', ' ')
			cls.prefLabel = locstr(cls_label, lang='en')
		_instances = cls.instances()
		for _instance in _instances:
			ins_label = _instance.prefLabel[0].replace('_', ' ')
			_instance.prefLabel = locstr(ins_label, lang='en')


if __name__ == '__main__':
	remove_label_underline(csdms)
	csdms.save(file='csdms-names-new.owl', format="rdfxml")
	name_to_label(hydrology)
	hydrology.save(file='hydrology-new.owl', format="rdfxml")
