#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/7/12 19:45

from rdflib import BNode, Literal
from rdflib.namespace import RDF, RDFS, SKOS, OWL, DCTERMS
from owlready2 import *
import types
import json

ont_uri = 'http://www.egc.org/ont/model/geospatial'
skos_file = 'file://skos.rdf'

onto = get_ontology(ont_uri)
skos = get_ontology(skos_file).load()
onto.imported_ontologies.append(skos)
# skos_ns = skos.get_namespace(base_iri='http://www.w3.org/2004/02/skos/core')
ont_cls = ['Contact', 'TechnicalSpecs', 'InputOutput', 'Input', 'Output', 'Process', 'Testing', 'Other', 'Component',
           'Publication']

# create an ontology class
with onto:
	class GeoSpatialModel(Thing):
		pass


	class Article(Thing):
		pass


	class StudyArea(Thing):
		pass


	class has_article(ObjectProperty):
		domain = [GeoSpatialModel]
		range = [Article]


	class has_study_area(GeoSpatialModel >> StudyArea):
		pass


	class has_author(Article >> str):
		pass

for idx, cls in enumerate(ont_cls):
	with onto:
		ont_cls[idx] = types.new_class(cls, (Thing,))
# superclass
# print(GeoSpatialModel.is_a)
# subclasses
# print(GeoSpatialModel.descendants())
# print(onto.Contact.is_a)
# print(onto['Contact'].is_a)
mycontact = onto.Contact('mycontact')  # individual
model1 = onto.GeoSpatialModel('model1')
# blank node: article1
model1.has_article = [Article(has_author=['houzw'], altLabel=locstr("Un commentaire en Français", lang="fr"))]
onto.Article.instances()
print(model1.has_article)
article_1 = Article('article_1')
article_1.has_author.append("hzw")
article_1.__getattr__("has_author").append("hzw2")
# print(onto.annotation_properties())
# print(skos.annotation_properties())  # generator 生成器
# print(list(skos.annotation_properties()))

onto.Contact.altLabel = "Contact anno"  # 在生成的本体中会显示为 skos:altLabel

# onto.save(file='owl_test.owl', format="rdfxml")
print(onto.search_one(iri="*Contact2", subclass_of=Thing))
print(list(article_1.get_properties()))

with onto:
	types.new_class('contact', (DataProperty,))
onto.contact.range=str

print(list(onto.data_properties()))
