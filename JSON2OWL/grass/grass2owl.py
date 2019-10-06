#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/7 22:25
from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

# import sys
# sys.setrecursionlimit(1000000)

module_uri = 'http://www.egc.org/ont/process/grass'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)

print('ontologies imported')
with onto:
	# print(gb.GeoprocessingFunctionality)
	class GrassTool(gb.GeoprocessingFunctionality):
		pass


	class StandardCategoryTool(GrassTool):
		pass


	class TopicCategoryTool(GrassTool):
		pass


	class GrassInput(gb.InputData):
		pass


	class GrassOutput(gb.OutputData):
		pass


	class GrassOption(gb.Option):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('GRASS GIS Tools')
import datetime

onto.metadata.created.append(datetime.datetime.today())
onto.metadata.versionInfo.append('7.5')


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
		if onto.__getattr__(option) is None:
			OWLUtils.create_onto_class(onto, option, prop_type)
		return option
	else:
		return _prop


def handle_parameters(tool, param):
	# 部分parameter不包含isInputFile等属性
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = GrassInput(prefLabel=locstr(param['parameter'], lang='en'))
		# p = GrassInput(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.inputData.append(p)
		p.isInputFile = param['isInputFile']
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = GrassOutput(prefLabel=locstr(param['parameter'], lang='en'))
		# p = GrassOutput(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.outputData.append(p)
		p.isOutputFile = param['isOutputFile']
	else:
		p = GrassOption(prefLabel=locstr(param['parameter'], lang='en'))
		# p = GrassOption(0, prefLabel=locstr(param['parameter'], lang='en'))
		tool.option.append(p)
	p.flag = param['flag']
	p.parameterName = param['parameter']
	if 'dataType' in param.keys():
		p.datatypeInString.append(param['dataType'])
	p.description.append(param['explanation'])
	if 'defaultValue' in param.keys():
		if param['defaultValue'] is not None: p.defaultValue = param['defaultValue']
	p.isOptional = param['isOptional']
	if 'alternatives' in param.keys():
		if param['alternatives']:
			for value in param['alternatives']:
				p.availableValue.append(value)

def handle_also(also_items):
	for also in also_items:
		# alsoToolClass = tool_class(also)
		# alsotool = alsoToolClass(also, prefLabel=locstr(also, lang='en'))
		for item in also.items():
			_tool = item[0]
			also_tools = item[1]
			for also_tool in also_tools:
				if onto[also_tool]:
					_tool.seeAlso.append(onto[also_tool])


def handle_task(tool, tool_name, en_str, _keywords, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in _keywords:
			task_cls = config.get('task', task_item)
			# print(task_cls)
			short_name = tool_name.split('.', maxsplit=1)[0]
			task_name = config.get('tools', short_name) + '_' + tool_name.split('.', maxsplit=1)[1]
			task_name = task_name.replace('.', '_')
			# avoid duplicate
			if not task[task_name + "_task"]:
				task_ins = task[task_cls](task_name + "_task", prefLabel=locstr(en_str + " task", lang='en'))
				task_ins.description.append(locstr(des, lang='en'))
				task_ins.isAtomicTask = True
			else:
				task_ins = task[task_name + "_task"]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.processingTool) is False:
				task_ins.processingTool.append(tool)


def handle_applcation():
	config = OWLUtils.get_config(module_path + '/config.ini')
	for k, v in config.items('application'):
		for _tool in v.split(','):
			_tool = _tool.strip()
			tools = [_tool]
			if str(_tool).endswith('*'):
				tools = onto.search(iri=module_uri + '#' + _tool)
			for __tool in tools:
				if onto[__tool] is not None:
					OWLUtils.application_category(onto[__tool], [], k, [])


def tool_class(tool_name):
	short_name = tool_name.split('.', maxsplit=1)[0]
	config = OWLUtils.get_config(module_path + '/config.ini')
	tool_cls = str(config.get('tools', short_name)).capitalize() + 'Tool'
	return OWLUtils.create_onto_class(onto, tool_cls, StandardCategoryTool)


def topic_classes():
	config = OWLUtils.get_config(module_path + '/config.ini')
	for k, v in config.items('application'):
		k = Preprocessor.to_upper_camel_case(k, True)
		topic_cls = OWLUtils.create_onto_class(onto, k, TopicCategoryTool)
		for _tool in v.split(','):
			_tool = _tool.strip()
			if onto[_tool] is not None:
				onto[_tool].is_a.append(topic_cls)


def map_to_owl(json_data):
	"""mapping json data to ontology properties"""
	tool_alsoes = []
	for item in json_data:
		name = item['name']
		if not name: continue
		if str(name).strip().find(' ') > 0: return
		# if str(name).strip().find(' ') > 0: continue
		# create or find tool class
		toolClass = tool_class(name)
		tool = toolClass(name, prefLabel=locstr(name, lang='en'))
		# tool = GrassTool(name, prefLabel=locstr(name, lang='en'))
		tool.isToolOfSoftware.append(cyber.GRASS_GIS)
		tool.identifier = name
		tool.manualPageURL.append(item['manual_url'])
		if 'addons' in item['manual_url']:
			tool.isAddon = True
		tool.description.append(locstr(item['description'], lang='en'))
		if item['source_code']: tool.sourceCodeURL.append(item['source_code'])
		tool.comment.append(item['notes'])
		tool.authors.append(OWLUtils.join_keywords(item['authors']))
		tool.definition.append(item['definition'])
		keywords = item['keywords']
		# tool.keywords.append(OWLUtils.join_keywords(item['keywords']))
		# tool.subject.append(OWLUtils.join_keywords(item['keywords']))
		# keywords and name
		# keywords.extend(name.split('.')[1:])
		OWLUtils.link_to_domain_concept( tool, keywords)

		tool.commandLine.append(item['synopsis'])
		r = re.match('[a-z.]+ ', item['synopsis'])
		if r: tool.executable = str(r.group()).strip()

		see_also_items = {}
		for also in item['see_also']:
			if '.' not in also: continue
			see_also_items[tool] = [also]
			tool_alsoes.append(see_also_items)
		for parameter in item['parameters']:
			handle_parameters(tool, parameter)
		handle_task(tool, name, name, item['keywords'], item['description'])
	handle_also(tool_alsoes)
	handle_applcation()
	topic_classes()


if __name__ == '__main__':
	module_path = os.path.dirname(__file__)
	with open(module_path + '/grass_edited.json', 'r') as f:
		jdata = json.load(f)  # list
	# print(len(jdata))
	# otherwise will report stack overflow exception
	size = 1024 * 1024 * 1024 * 10
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()

	onto.save(file='grass.owl', format="rdfxml")
	# update task ontology
	task.save()
	geospatial.save()
	print('GRASS Done!')
