#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/9/10 22:42
from owlready2 import *
from os import path

# <owl:imports rdf:resource="http://data.ordnancesurvey.co.uk/ontology/geometry/"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/base/props"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/domain/dta"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/domain/hydrology"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/vocab/cf"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/vocab/csdms"/>
# <owl:imports rdf:resource="http://www.egc.org/ont/vocab/gis"/>
# <owl:imports rdf:resource="http://www.w3.org/2004/02/skos/core"/>
# <owl:imports rdf:resource="https://gcmdservices.gsfc.nasa.gov/kms/concept"/>
onto_path.append(path.normpath(path.dirname(__file__)) + '/')
geospatial = get_ontology('/geospatial_vocab_all.owl').load(only_local=True)
skos = get_ontology('/skos.rdf').load(only_local=True)
# dc = get_ontology('/dcterms.rdf').load(only_local=True)
geospatial.imported_ontologies.append(skos)


# geospatial.imported_ontologies.append(dc)

def uri2label():
	for cls in geospatial.classes():
		cls_label = cls.prefLabel
		# print(ind_label)
		if len(cls_label) == 0:
			cls.prefLabel.append(locstr(cls.name.replace('_', ' '), lang='en'))
		for ind in cls.instances():
			name = ind.name
			ind_label = ind.prefLabel
			# print(ind_label)
			if len(ind_label) == 0:
				ind.prefLabel.append(locstr(name.replace('_', ' '), lang='en'))
	geospatial.save()

if __name__ == "__main__":
	threading.stack_size(2000000)
	thread = threading.Thread(target=uri2label())
	thread.start()
