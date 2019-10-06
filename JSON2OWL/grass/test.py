#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/7/13 19:12

import json
import os
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

module_path = os.path.dirname(__file__)
with open(module_path + '/grass.json', 'r') as f:
	jdata = json.load(f)  # list

for i,d in enumerate(jdata):
	# if i>5: break
	name = OWLUtils.toolname_underline(d['name'])
	task = OWLUtils.task_name(name)
	print(task)
