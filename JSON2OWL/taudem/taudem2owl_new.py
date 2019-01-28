#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/9/10 18:58
from owlready2 import *
import json
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

model_uri = 'http://www.egc.org/ont/process/taudem'
onto = get_ontology(model_uri)
onto,  gb, task, data = OWLUtils.load_common_for_process_tool(onto)


# print(onto.imported_ontologies)

def get_property(option, prop_type):
	"""
		根据配置查找对应的属性，没有则创建新的属性

	Args:
		option: property name
		prop_type: ObjectProperty or DataProperty

	Returns: created property name

	"""
	config = OWLUtils.get_config(module_path+'/config.ini')
	_prop = OWLUtils.get_option(config, 'taudem', option)
	# 返回配置的属性或是已有的属性（has[Name]）
	if _prop is not None:
		return _prop
	else:
		_prop = gb.__getattr__('has' + option.capitalize())
		if _prop is None:
			OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
	return 'has' + option.capitalize()


# if prop is None:
# 	OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
# 	return 'has' + option.capitalize()
# else:
# 	return prop


def get_format(option):
	config = OWLUtils.get_config(module_path+'/config.ini')
	_prop = OWLUtils.get_option(config, 'format', option)
	return _prop


with onto:
	class TauDEMAnalysis(gb.ProcessingTool):
		pass


	class TauDEMInput(gb.InputData):
		pass


	class TauDEMOutput(gb.OutputData):
		pass


	class TauDEMOption(gb.Option):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/taudem.json', 'r') as f:
	jdata = json.load(f)  # list

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('TauDEM Tools')
import datetime

onto.metadata.created.append(datetime.datetime.today())


def handle_params(tool_param, param_item):
	# 具体参数
	for itemK, itemV in param_item.items():
		# 数据格式
		if itemK == 'dataType' and get_format(itemV) is not None:
			tool_param.supportsDataFormat.append(data[get_format(itemV)])
		_prop = get_property(itemK, DataProperty)
		try:
			if type(itemV) == list:
				tool_param.__getattr__(_prop).append(''.join(itemV))
			else:
				tool_param.__getattr__(_prop).append(itemV)
		except AttributeError:
			if type(itemV) == list:
				tool_param.__setattr__(_prop, ''.join(itemV))
			else:
				tool_param.__setattr__(_prop, itemV)


def handle_task(tool_name, en_str,des):
	if task[tool_name+"_task"] is None:
		task_ins = task['HydrologicalAnalysis'](tool_name+"_task", prefLabel=locstr(en_str+" task", lang='en'))
		task_ins.description.append(locstr(des,lang='en'))
	# tool.usedByTask.append(task_ins)
	# task_ins.hasProcessingTool.append(tool)
	else:
		task_ins = task[tool_name+"_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.hasProcessingTool) is False:
		task_ins.hasProcessingTool.append(tool)


for d in jdata:
	# 实例
	name = d['title'].strip().replace(' ', '_')
	tool = onto.TauDEMAnalysis(name, prefLabel=locstr(d['title'], lang='en'))
	tool.isToolOfSoftware.append(gb.TauDEM)
	for k, v in d.items():
		# 外层, 参数
		if k == 'parameter' and type(v) == list:
			for i, item in enumerate(v):
				localname = v[i]['parameter']
				if localname.lower().startswith('input_', 0, len('input_')):
					param = TauDEMInput(localname, prefLabel=locstr(localname.replace('_', ' '), lang='en'))
					tool.hasInputData.append(param)
					handle_params(param, item)
				elif localname.lower().startswith('output_', 0, len('output_')):
					param = TauDEMOutput(localname, prefLabel=locstr(localname.replace('_', ' '), lang='en'))
					tool.hasOutputData.append(param)
					handle_params(param, item)
				else:
					o = TauDEMOption(localname, prefLabel=locstr(localname.replace('_', ' '), lang='en'))
					tool.hasOption.append(o)
					handle_params(o, item)
		else:
			prop = get_property(k, DataProperty)
			if not v:
				continue
			if type(v) == list:
				if len(v) > 0:
					tool.__getattr__(prop).append(''.join(v))
			else:
				tool.__getattr__(prop).append(v)
	# task
	handle_task(name, d['title'], ' '.join(d['summary']))

onto.save(file='taudem.owl', format="rdfxml")
# update task ontology
task.save()
print('TAUDEM Done!')
