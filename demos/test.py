#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/2 22:57
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

import json
from collections import namedtuple


def _json_object_hook(d):
	return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
	return json.loads(data, object_hook=_json_object_hook)

l = ['A','b','c']
print('a' in l)
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
name = re.sub("^Tool [0-9: ]*", '', 'Tool Residual Analysis (Grid)').strip()
name2 = re.sub("^Tool [0-9: ]*", '', 'Residual Analysis').strip()
name =OWLUtils.toolname_underline(name)
print(name)
a= 'fffff'
print(' '.join(a))