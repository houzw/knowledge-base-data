#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/9/14 15:26
from owlready2 import *
import json
module_path = os.path.dirname(__file__)
data = get_ontology('/data.owl').load(only_local=True)

with open(module_path + '/arcgis.json', 'r') as f:
	jdata = json.load(f)  # list

for d in jdata:
	for parameter in d['parameters']:
		datatype = parameter['dataType']
		if datatype:
			datatypes = []
			if ";" in datatype:
				datatypes = str(datatype).split(";")
			elif "|" in datatype:
				datatypes = str(datatype).split("|")
			elif "," in datatype:
				datatypes = str(datatype).split(",")
			if len(datatypes) > 0:
				for dt in datatypes:
					dt = dt.strip().lower().replace(' ', '_')
					if not data[dt]:
						data.ArcGISDataType(dt, prefLabel=locstr(datatype, lang='en'))
			else:
				dt = datatype.strip().lower().replace(' ', '_')
				if not data[dt]:
					data.ArcGISDataType(dt, prefLabel=locstr(datatype, lang='en'))
