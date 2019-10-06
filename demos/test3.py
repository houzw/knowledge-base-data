#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# https://rdflib.readthedocs.io/en/stable/_modules/rdflib/collection.html
# time: 2019/9/21 19:42
from owlready2 import *
from os import path

from JSON2OWL.OwlConvert.OwlUtils import OWLUtils as ou

onto = get_ontology('www.test.org#')
onto, _list = ou.resources_2_rdf_list(onto,['a','b','c','d'])
onto.save('onto_test.owl')



