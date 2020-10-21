#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/9/10 18:58
from owlready2 import *
import json
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

module_uri = 'http://www.egc.org/ont/process/taudem'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)

print('ontologies imported')


def get_property(option, prop_type):
	"""
		根据配置查找对应的属性，没有则创建新的属性

	Args:
		option: property name
		prop_type: ObjectProperty or DataProperty

	Returns: created property name

	"""
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'taudem', option)
	# 返回配置的属性或是已有的属性（has[Name]）
	if _prop is not None:
		return _prop
	else:
		_prop = gb.__getattr__(option)
		if _prop is None:
			OWLUtils.create_onto_class(onto, option, prop_type)
	return option


def get_format(option):
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'format', option)
	return _prop


def get_task_class(tool_name):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tool_cls = ''  # only one
	for k, v in config.items('task'):
		if tool_name in v:
			tool_cls = k
	return tool_cls


with onto:
	class TauDEMAnalysis(gb.GeoprocessingFunctionality):
		pass


	class TauDEMInput(cyber.Input):
		pass


	class TauDEMOutput(cyber.Output):
		pass


	class TauDEMOption(cyber.Option):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('TauDEM Tools')
import datetime

onto.metadata.created.append(datetime.datetime.today())
onto.metadata.versionInfo.append('5.3')


def handle_params(tool_param, param_item):
	# 具体参数
	for itemK, itemV in param_item.items():
		# 数据格式
		if itemK == 'dataType' and get_format(itemV) is not None:
			tool_param.supportsDataFormat.append(data[get_format(itemV)])
			tool_param.datatype.append(OWLUtils.get_datatype_iris(itemV))
		_prop = get_property(itemK, DataProperty)
		if type(itemV) == list:
			itemV = ''.join(itemV)
		OWLUtils.set_data_property(tool_param, _prop, itemV)


def handle_task(tool, tool_name, en_str, des):
	if task[tool_name + "_task"] is None:
		# title
		cls = get_task_class(en_str)
		task_ins = task[cls](tool_name + "_task", prefLabel=locstr(en_str + " task", lang='en'))
		task_ins.is_a.append(task['TerrainAnalysis'])
		task_ins.description.append(locstr(des, lang='en'))
		task_ins.isAtomicTask = True
	else:
		task_ins = task[tool_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.processingTool) is False:
		task_ins.processingTool.append(tool)


def map_to_owl(json_data):
	for d in json_data:
		"""mapping json data to ontology properties"""
		# instance 实例
		name = Preprocessor.name_underline(d['name'])
		toolClass = tool_class(d['name'])
		tool = toolClass(name, prefLabel=locstr(d['name'], lang='en'))
		tool.isToolOfSoftware.append(cyber.TauDEM)
		tool.identifier = name
		description = OWLUtils.join_list(d['description'])
		keywords = OWLUtils.to_keywords(description)
		keywords.extend(name.replace('_', ' ').split(' '))
		# keywords=name.replace('_', ' ').split(' ')
		OWLUtils.link_to_domain_concept(tool, keywords)

		for k, v in d.items():
			# 外层, 参数
			if (k in ['parameters', 'options']) and type(v) == list:
				for i, item in enumerate(v):
					param = None
					# localname = v[i]['parameterName']
					localname = Preprocessor.space_2_underline(item['parameterName'])
					_label = localname.replace('_', ' ')
					if item['isInputFile']:
						param = TauDEMInput(localname, prefLabel=locstr(_label, lang='en'))
						# param = TauDEMInput(prefLabel=locstr(_label, lang='en'))
						# input geo data ? rule: format-> geoformat->geo data
						tool.input.append(param)
						handle_params(param, item)
						param.isInput = True
					elif item['isOutputFile']:  # localname.lower().startswith('output_', 0, len('output_')):
						param = TauDEMOutput(localname, prefLabel=locstr(_label, lang='en'))
						# param = TauDEMOutput(prefLabel=locstr(_label, lang='en'))
						tool.output.append(param)
						handle_params(param, item)
						param.isOutput = True
					else:
						param = TauDEMOption(localname, prefLabel=locstr(_label, lang='en'))
						# param = TauDEMOption(prefLabel=locstr(localname.replace('_', ' '), lang='en'))
						tool.option.append(param)
						handle_params(param, item)
					OWLUtils.link_to_domain_concept(param, _label)
					param.identifier = localname
			else:
				prop = get_property(k, DataProperty)
				if not v:
					continue
				if type(v) == list and len(v) > 0:
					v = ''.join(v)
				OWLUtils.set_data_property(tool, prop, v)
		# task
		handle_task(tool, name, d['name'], description)
		OWLUtils.application_category(tool, 'Geomorphometry', 'digital terrain analysis', 'hydrology')


def tool_class(tool_name):
	tool_cls = get_task_class(tool_name)
	return OWLUtils.create_onto_class(onto, tool_cls, TauDEMAnalysis)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/taudem.json', 'r') as f:
		jdata = json.load(f)  # list
	# otherwise will report stack overflow exception
	threading.stack_size(200000)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='taudem.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('TAUDEM Done!')
