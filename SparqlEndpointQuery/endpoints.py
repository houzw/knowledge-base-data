#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/24 17:50
from enum import Enum, unique


@unique
class SparqlEndpoints(Enum):
	# https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#SPARQL_endpoint
	Wikidata = ('https://query.wikidata.org/sparql', 'Accept: application/sparql-results+json')
	dbpedia0 = ('http://dbpedia0.gstore-pku.com/', '')
	freebase = ('http://freebase.gstore-pku.com/', '')
	dbpedia = ('http://dbpedia.gstore-pku.com/', '')
	openkg = ('http://openkg.gstore-pku.com/', '')

	def __init__(self, url, header):
		self.url = url
		self.header = header
