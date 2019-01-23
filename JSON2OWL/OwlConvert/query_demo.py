#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/20 22:00

import rdflib

# from owlready2 import *
# my_world = World()
# my_world.get_ontology("file://DataDescription.owl").load() #path to the owl file is given here
# # sync_reasoner(my_world)  #reasoner is started and synchronized here
# graph = my_world.as_rdflib_graph()
#
# sparql = """
# """
# resultsList  = graph.query(sparql)
# for item in resultsList:
#     s = str(item['s'].toPython())
#     s = re.sub(r'.*#',"",s)

g = rdflib.Graph()
g.parse("DataDescription.owl")
qres = g.query("""
SELECT ?format
WHERE {?format a data:RasterFormat.}
""", initNs={'data': 'http://www.egc.org/ont/data#'})
for row in qres:
	print("%s" % row)
