#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/2/20 22:01
# https://pypi.org/project/pyshacl/

from pyshacl import validate
from rdflib import Graph

graph = Graph()
graph.parse('shacl_test.ttl')
r = validate('saga.owl', graph)
conforms, results_graph, results_text = r
