#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/12/30 11:07

from rdflib import Graph
from rdflib.term import BNode
from rdflib.term import Literal
from rdflib.collection import Collection

g = Graph()
c = Collection(g, BNode(), [Literal("1"), Literal("2"), Literal("3"), Literal("4")])
# g.serialize('listdemo.ttl',format='turtle')
g.serialize('listdemo.owl',format='xml')