#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# https://rdflib.readthedocs.io/en/stable/_modules/rdflib/collection.html
# time: 2019/9/21 19:42
from owlready2 import *
from os import path

from JSON2OWL.OwlConvert.OwlUtils import OWLUtils as ou

# onto = get_ontology('www.test.org#')
# onto, _list = ou.resources_2_rdf_list(onto,['a','b','c','d'])
# onto.save('onto_test.owl')
import string,random
from secrets import randbelow
print(randbelow(3))
seeds = string.digits
random_str = random.choices(seeds, k=0)
print("".join(random_str))

# alternatives = ['0-9999']
# alternatives = ['-9999-9999']
alternatives = ['90-<max integer on system would make sense>']

if re.match('[-0-9]+-[0-9]+', alternatives[0]):
	minimum = alternatives[0].rsplit('-',1)[0]
	maximum = alternatives[0].rsplit('-',1)[1]
	print(minimum)
	print(maximum)
elif re.match('[-0-9]+-[a-zA-Z<> ]+', alternatives[0]):
	minimum = alternatives[0].rsplit('-')[0]
	print(minimum)
