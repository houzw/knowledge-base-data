#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/7 22:25
from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

model_uri = 'http://www.egc.org/ont/process/grass'
onto = get_ontology(model_uri)
onto, shacl, skos, dcterms, props = OWLUtils.load_common(onto)
onto, gb, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class GrassTool(gb.GeoprocessingTool):
		pass


	class GrassInput(gb.InputData):
		pass


	class GrassOutput(gb.OutputData):
		pass


	class GrassOption(gb.Option):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/grass.json', 'r') as f:
	jdata = json.load(f)  # list

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('GRASS GIS Tools')
import datetime

onto.metadata.created.append(datetime.datetime.today())


def get_property(option, prop_type):
	"""
		根据配置查找对应的属性，没有则创建新的属性

	Args:
		option: property name
		prop_type: ObjectProperty or DataProperty

	Returns: created property name

	"""
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'grass', option)
	if _prop is None:
		if onto.__getattr__('has' + option.capitalize()) is None:
			OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
		return 'has' + option.capitalize()
	else:
		return _prop


def handle_parameters(param):
	# 部分parameter不包含isInputFile等属性
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = GrassInput(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.hasInputData.append(p)
		p.isInputFile = param['isInputFile']
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = GrassOutput(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.hasOutputData.append(p)
		p.isOutputFile = param['isOutputFile']
	else:
		p = GrassOption(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.hasOption.append(p)
	p.hasFlag.append(param['flag'])
	p.hasParameterName=param['parameter']
	if 'dataType' in param.keys():
		p.hasDataTypeStr.append(param['dataType'])
	p.description.append(param['explanation'])
	if 'defaultValue' in param.keys():
		if param['defaultValue'] is not None: p.hasDefaultValue = param['defaultValue']
	p.isOptional = param['optional']
	if 'alternatives' in param.keys():
		if param['alternatives']:
			p.hasAlternatives.append(', '.join(param['alternatives']))

def handle_task(tool_name, en_str, keywords,des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in keywords:
			task_cls = config.get('task', task_item)
			# print(task_cls)
			short_name = tool_name.split('.', maxsplit=1)[0]
			task_name = config.get('tools', short_name) + '_' + tool_name.split('.', maxsplit=1)[1]
			task_name = task_name.replace('.', '_')
			# avoid duplicate
			if not task[task_name+"_task"]:
				task_ins = task[task_cls](task_name+"_task", prefLabel=locstr(en_str+" task", lang='en'))
				task_ins.description.append(locstr(des, lang='en'))
			else:
				task_ins = task[task_name+"_task"]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.hasProcessingTool) is False:
				task_ins.hasProcessingTool.append(tool)

for d in jdata:
	name = d['name']
	if not name: continue
	if str(name).strip().find(' ') > 0: continue
	tool = GrassTool(name, prefLabel=locstr(name, lang='en'))
	tool.isToolOfSoftware.append(gb.GRASS_GIS)
	tool.hasIdentifier = name
	tool.hasManualPageURL.append(d['manual_url'])
	tool.description.append(locstr(d['description'], lang='en'))
	if d['source_code']: tool.hasSourceCodeURL.append(d['source_code'])
	tool.abstract.append(d['notes'])
	tool.hasAuthors.append(', '.join(d['authors']))
	tool.definition.append(d['definition'])
	tool.hasKeywords.append(', '.join(d['keywords']))
	tool.hasSyntax.append(d['synopsis'])
	r = re.match('[a-z.]+ ', d['synopsis'])
	if r: tool.hasExecutable = str(r.group()).strip()
	for also in d['see_also']:
		alsotool = GrassTool(also, prefLabel=locstr(also, lang='en'))
		tool.seeAlso.append(alsotool)
	for parameter in d['parameters']:
		handle_parameters(parameter)
	handle_task(name, name, d['keywords'],d['description'])

onto.save(file='grass.owl', format="rdfxml")
# update task ontology
task.save()
print('GRASS Done!')
