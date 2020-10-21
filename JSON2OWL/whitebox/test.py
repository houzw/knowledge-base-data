#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/10/28 8:19
import os
import re
import json
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

def map_to_owl(json_data):
	for d in json_data:
		name = d['description']
		re.search('(Creates the|Calculates a)[a-zA-Z \-](from)', name)
		new_name = name.split('from')[0]
		print(re.sub('Creates (the|an|a)', '',new_name))
		print(re.sub('Calculates (the|an|a)', '',new_name))
		new_name.replace('Identifies the', '')
		new_name.replace('Estimates the', '')
		new_name.replace('Measures the', '')
		new_name.replace('Converts a', '')
		new_name.replace('Aggregates a', '')
		print(new_name)
if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/whitebox0703.json', 'r') as f:
		jdata = json.load(f)  # list
	map_to_owl(jdata)