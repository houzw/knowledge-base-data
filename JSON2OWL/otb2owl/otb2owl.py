#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/2/20 22:11

# TODO
from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor
import datetime

module_uri = 'http://www.egc.org/ont/process/otb'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class OTBTool(gb.GeoprocessingFunctionality):
		pass


	class OTBInput(gb.InputData):
		pass


	class OTBOutput(gb.OutputData):
		pass


	class OTBConstraint(gb.Constraint):
		pass


	class OTBAvailableChoice(gb.AvailableChoice):
		pass


	class OTBOption(gb.Option):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('Orfeo-Toolbox Tools')

onto.metadata.created.append(datetime.datetime.today())
onto.metadata.versionInfo.append('6.6.1')


def handle_task(tool, category, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	task_cls = config.get('task', category)
	# avoid duplicate
	i_task_name = task_name.replace(' ', '_')
	if not task[i_task_name + "_task"]:
		task_ins = task[task_cls](i_task_name + "_task", prefLabel=locstr(task_name + " task", lang='en'))
		task_ins.isAtomicTask = True
	else:
		task_ins = task[i_task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.processingTool) is False:
		task_ins.processingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def get_datatype(k):
	config = OWLUtils.get_config(module_path + '/config.ini')
	_type = OWLUtils.get_option(config, 'datatype', k)
	if _type is None:
		return 'http://www.w3.org/2001/XMLSchema#string'
	else:
		return _type


def handle_parameters(tool, param):
	# 部分parameter不包含isInputFile等属性
	p = None
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = OTBInput(prefLabel=locstr(param['parameterName'], lang='en'))
		# p = OTBInput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.inputData.append(p)
		p.isInputFile = param['isInputFile']
		p.supportsDataFormat.append(data.GeoTIFF)
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = OTBOutput(prefLabel=locstr(param['parameterName'], lang='en'))
		# p = OTBOutput(0, prefLabel=locstr(param['parameterName'], lang='en'))
		tool.outputData.append(p)
		p.isOutputFile = param['isOutputFile']
		p.supportsDataFormat.append(data.GeoTIFF)
	p.flag = param['flag']
	p.parameterName = param['parameterName']
	if 'dataType' in param.keys() and param['dataType']:
		p.datatypeInString.append(param['dataType'])
	p.description.append(locstr(' '.join(param['explanation']), lang='en'))

# p.isOptional = param['isOptional'] # no this information in document

def handle_options(tool, param, _onto):
	o = OTBOption(prefLabel=locstr(param['parameterName'], lang='en'))
	# p = OTBOption(0, prefLabel=locstr(param['parameterName'], lang='en'))
	tool.option.append(o)
	sc = OTBConstraint(comment=locstr("shacl data constraint", lang='en'))
	# sc = OTBConstraint(0, comment=locstr("shacl data constraint", lang='en'))
	o.property.append(sc)
	o.parameterName = param['parameterName']
	if 'dataType' in param.keys() and param['dataType']:
		if param['dataType'] == "Choices":
			o.datatypeInString.append('String')
			o.datatypeInString.append('String')
		o.datatypeInString.append(param['dataType'])
		sc.datatype.append(IRIS[get_datatype(param['dataType'])])
	o.description.append(''.join(param['explanation']))
	# p.isOptional = param['isOptional']
	if 'availableChoices' in param.keys() and param['availableChoices']:
		o, onto = OWLUtils.handle_choices(o, param['parameterName'], param['availableChoices'], OTBAvailableChoice, _onto)


def map_to_owl(json_data):
	for d in json_data:
		"""mapping json data to ontology properties"""
		if d['category'] == 'Deprecated':
			continue
		name_str = d['name']
		toolClass = tool_class(d['category'])
		tool = toolClass(name_str, prefLabel=locstr(d['label'], lang='en'))
		OWLUtils.application_category(tool, [], d['category'], [])
		tool.isToolOfSoftware.append(cyber.OrfeoToolBox)
		tool.identifier = name_str
		tool.manualPageURL.append(normstr(d['manual_url']))
		tool.executable = d['command']
		tool.description.append(locstr(d['description'], lang='en'))
		tool.definition.append(d['definition'])

		keywords = OWLUtils.to_keywords(d['description'])
		keywords.extend(d['label'].split(" "))
		# keywords=d['label'].split(" ")
		OWLUtils.link_to_domain_concept(tool, keywords)

		if d['authors']:
			tool.authors.append(d['authors'])
		for ex in d['example']:
			tool.example.append(ex)
		handle_task(tool, d['category'], d['label'], d['description'])
		for parameter in d['parameters']:
			handle_parameters(tool, parameter)
		for option in d['options']:
			handle_options(tool, option, onto)


def tool_class(category):
	tool_cls = category.replace(' ', '') + 'Tool'
	return OWLUtils.create_onto_class(onto, tool_cls, OTBTool)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/otb.json', 'r') as f:
		jdata = json.load(f)  # list
	# print(len(jdata))
	# otherwise will report stack overflow exception
	threading.stack_size(2000000)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='otb.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('OTB Done!')
