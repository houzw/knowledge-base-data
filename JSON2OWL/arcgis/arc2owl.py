#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/7 22:25

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
import datetime

model_uri = 'http://www.egc.org/ont/process/arcgis'
onto = get_ontology(model_uri)
onto, shacl, skos, dcterms, props = OWLUtils.load_common(onto)
onto, gb, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class ArcGISTool(gb.GeoprocessingTool):
		pass


	class ArcGISInput(gb.InputData):
		pass


	class ArcGISOutput(gb.OutputData):
		pass


	class ArcGISOption(gb.Option):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/arcgis.json', 'r') as f:
	jdata = json.load(f)  # list

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('ArcGIS Tools')

onto.metadata.created.append(datetime.datetime.today())


def handle_task(full_name, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	task_types = re.findall("\([a-zA-Z0-9*\-' ]+\)", full_name)
	# print(full_name)
	if len(task_types) > 1:
		tool.hasKeywords.append(task_types[0].replace('(', '').replace(')', ''))
		task_type = re.findall("\([0-9a-zA-Z*\-' ]+\)", full_name)[-1].replace('(', '').replace(')', '')
	else:
		task_type = re.findall("\([0-9a-zA-Z*\-' ]+\)", full_name)[0].replace('(', '').replace(')', '')
	task_cls = config.get('task', task_type)
	tool.hasKeywords.append(task_type)
	# avoid duplicate
	if not task[task_name + "_task"]:
		task_ins = task[task_cls](task_name + "_task", prefLabel=locstr(task_name.replace('_', ' ') + " task", lang='en'))
	else:
		task_ins = task[task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.hasProcessingTool) is False:
		task_ins.hasProcessingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def handle_parameters(param):
	# 部分parameter不包含isInputFile等属性
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = ArcGISInput( prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISInput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.hasInputData.append(p)
		p.isInputFile = param['isInputFile']
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = ArcGISOutput(prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISOutput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.hasOutputData.append(p)
		p.isOutputFile = param['isOutputFile']
	else:
		p = ArcGISOption( prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISOption(0, prefLabel=locstr(param['name'], lang='en'))
		tool.hasOption.append(p)
	p.hasParameterName=param['name']
	if 'type' in param.keys() and param['type']:
		p.hasDataTypeStr.append(param['type'])
	p.description.append(param['desc'])
	p.isOptional = param['isOptional']
	# p.isMandatory = not param['isOptional']
	datatype = param['type']
	if datatype:
		datatypes = []
		if ";" in datatype: datatypes = str(datatype).split(";")
		elif "|" in datatype: datatypes = str(datatype).split("|")
		elif "," in datatype: datatypes = str(datatype).split(",")
		if len(datatypes) > 0:
			for dt in datatypes:
				dt = dt.strip().lower().replace(' ', '_')
				if not data[dt]:
					data.ArcGISDataType(dt, prefLabel=locstr(datatype, lang='en'))
				p.hasDataType.append(data[dt])
		else:
			dt = datatype.strip().lower().replace(' ', '_')
			if not data[dt]:
				data.ArcGISDataType(dt, prefLabel=locstr(datatype, lang='en'))
			p.hasDataType.append(data[dt])


def handle_example(example):
	ex = 'Title: ' + example['title'] if example['title'] else ''
	ex = ex + '\n' + 'Description: ' + example['desc'] if example['desc'] else ex
	ex += '\n' + 'Code: \n' + example['code']
	return ex


for d in jdata:
	name_str = ''
	name = re.match("[0-9a-zA-Z\-/* ]+ (?=\([\w' ]+\))", d['name'])
	if name:
		name_str = name.group().strip().lower().replace(' ', '_').replace('/', '_')
	else:
		continue
	tool = ArcGISTool(name_str, prefLabel=locstr(name_str, lang='en'))
	tool.isToolOfSoftware.append(gb.ArcGIS_Desktop)
	tool.hasIdentifier = name_str
	# tool.hasManualPageURL.append(d['manual_url'])
	# tool.description.append(locstr(d['description'], lang='en'))
	tool.abstract.append(locstr(d['summary'], lang='en'))
	# tool.definition.append(d['definition'])
	tool.hasUsage.append(' '.join(d['usage']))
	tool.hasSyntax.append(d['syntax'])
	tool.example.append(handle_example(d['example']))
	handle_task(d['name'], name_str, d['summary'])
	for parameter in d['parameters']:
		handle_parameters(parameter)

onto.save(file='arcgis.owl', format="rdfxml")
# update task ontology
task.save()
# data.save()
print('ArcGIS Done!')
