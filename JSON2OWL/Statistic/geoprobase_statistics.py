#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/7/5 9:57

from owlready2 import *
from os import path
onto = get_ontology('file://geoprobase.owl').load(only_local=True)
triples = onto.get_triples(None,None,None)
print(len(triples))
