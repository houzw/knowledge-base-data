#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/8/20 21:28
import os
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

module_path = os.path.dirname(__file__)

config = OWLUtils.get_config(module_path + '/config.ini')
for k, v in config.items('application'):
	# print(k)
	print(type(v.split(',')))
