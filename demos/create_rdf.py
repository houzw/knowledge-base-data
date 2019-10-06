#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/9/25 9:19
from owlready2 import *

test_ont = get_ontology('http://www.test.org#')
rdf = get_ontology('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = get_ontology('http://www.w3.org/2000/01/rdf-schema#')
with test_ont:
	class Resource(Thing):
		namespace = rdfs
		isDefinedBy = 'http://www.w3.org/2000/01/rdf-schema#'
		label = "Resource"
		comment = "The class resource, everything."


	class Literal(Resource):
		namespace = rdfs
		isDefinedBy = 'http://www.w3.org/2000/01/rdf-schema#'
		label = "Literal"
		comment = "The class of literal values, eg. textual strings and integers."


	class List(Resource):
		isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
		namespace = rdf
		label = "List"
		comment = "The class of RDF Lists."


	class first(ObjectProperty):
		isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
		namespace = rdf
		label = "first"
		comment = "The first item in the subject RDF list."
		domain = [List]
		range = [Resource]


	class rest(ObjectProperty):
		isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
		namespace = rdf
		label = "rest"
		comment = "The rest of the subject RDF list after the first item."
		domain = [List]
		range = [List]

nil = List('nil', label='nil', comment='The empty list, with no items in it. If the rest of a list is nil then the list has no more items in it.', namespace=test_ont)
print(Resource)

l = ['a', 'b', 'c', 'd']
testl = List(0, namespace=test_ont)
print(nil)


def create_list(rdf_list, words):
	rdf_list.first = [Literal(words[0], namespace=test_ont)]
	if len(words) == 1:
		rdf_list.rest.append(nil)
		return rdf_list
	_rdf_list = List(0, namespace=test_ont)
	rdf_list.rest.append(create_list(_rdf_list, words[1:]))
	return rdf_list


create_list(testl, l)
print(testl)
print(testl.first)
print(testl.rest)
# test_ont.save("list_test.owl")
