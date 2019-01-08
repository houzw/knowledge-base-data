#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/3 16:04

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

model_uri = 'http://www.egc.org/ont/process/saga'
onto = get_ontology(model_uri)
onto, soft, geoprocessor, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class SagaTool(geoprocessor.Geoprocessor):
		pass


	class SagaParameter(geoprocessor.Parameter):
		pass


	class SagaInput(SagaParameter):
		pass


	class SagaOutput(SagaParameter):
		pass


	class SagaOption(geoprocessor.Option):
		pass


	class SagaConstraint(geoprocessor.Constraint):
		pass


	class SagaAvailableChoice(geoprocessor.AvailableChoice):
		pass

with open('saga.json', 'r') as f:
	jdata = json.load(f)  # list


def get_property(option, prop_type):
	"""
		根据配置查找对应的属性，没有则创建新的属性

	Args:
		option: property name
		prop_type: ObjectProperty or DataProperty

	Returns: created property name

	"""
	config = OWLUtils.get_config('config.ini')
	_prop = OWLUtils.get_option(config, 'saga', option)
	if _prop is None:
		if onto.__getattr__('has' + option.capitalize()) is None:
			OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
		return 'has' + option.capitalize()
	else:
		return _prop


def get_format(option):
	"""对应的数据格式"""
	config = OWLUtils.get_config('config.ini')
	_prop = OWLUtils.get_option(config, 'format', option)
	return _prop


def string_value(str_key, str_value):
	s_prop = get_property(str_key, DataProperty)
	if not str_value or str_value == '' or str_value == '-':
		pass
	else:
		tool.__getattr__(s_prop).append(str_value)


def handle_inout(item_value, in_or_out):
	for ioD in item_value:
		# print(ioD)
		io_name = ioD['name']
		if io_name is None:
			io_name = in_or_out
		# localname = OWLUtils.name_underline(ioD['identifier'])
		if in_or_out == 'input':
			param = SagaInput(prefLabel=locstr(io_name, lang='en'))
			# param =SagaInput('input_'+localname, prefLabel=locstr(io_name, lang='en'))
			tool.hasInputParameter.append(param)
		else:
			param = SagaOutput(prefLabel=locstr(io_name, lang='en'))
			# param =SagaOutput('output_'+localname, prefLabel=locstr(io_name, lang='en'))
			tool.hasOutputParameter.append(param)
		for k, v in ioD.items():
			if k == 'type' and get_format(v) is not None:
				param.supportsDataFormat.append(data[get_format(v)])
			if v is not None or v:
				p = get_property(k, DataProperty)
				if type(v) is str:
					v = v.strip()
				if v == {}:
					continue
				if param.__getattr__(p) is None or isinstance(param.__getattr__(p), bool):
					param.__setattr__(p, v)
				else:
					param.__getattr__(p).append(v)


def handle_options(option):
	op_name = option['name']
	if op_name is None:
		op_name = 'option'
	# localname = OWLUtils.name_underline(option['identifier'])
	# localname = OWLUtils.name_underline(op_name)
	indi = SagaOption( prefLabel=locstr(name, lang='en'))
	# indi = SagaOption('option_'+localname,prefLabel=locstr(name, lang='en'))
	tool.hasOption.append(indi)
	for k, v in option.items():
		if k == "constraints" and v is not None:
			constraint = SagaConstraint(prefLabel=locstr(option['name'], lang='en'))
			indi.hasConstraint.append(constraint)
			for itemK, itemV in v.items():
				# functional 属性不能使用append
				if itemK == 'availableChoices':
					for choice in itemV:
						availableChoices = SagaAvailableChoice(prefLabel=locstr(op_name + ' available choice', lang='en'))
						availableChoices.hasChoice.append(choice['choice'])
						if choice['description'] is not None and (choice['description'] != ' ' or choice['description'] != '-'):
							availableChoices.description.append(choice['description'].strip())
						constraint.hasAvailableChoice.append(availableChoices)
				else:
					p = get_property(itemK, DataProperty)
					# constraint.__getattr__(p)会返回 str,float,bool等类型？
					# 不能使用 append
					try:
						if option['type'] == 'Floating point':
							constraint.__getattr__(p).append(float(itemV))
						else:
							constraint.__getattr__(p).append(itemV)
					except AttributeError:
						if option['type'] == 'Floating point':
							constraint.__setattr__(p, float(itemV))
						else:
							constraint.__setattr__(p, itemV)
		elif k == "description" and v == "-":
			continue
		elif type(v) is str:
			v = OWLUtils.name_underline(v)
			p = get_property(k, DataProperty)
			indi.__getattr__(p).append(v)


def handle_task(tool_name, en_str, keywords):
	config = OWLUtils.get_config('config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in keywords:
			task_cls = config.get('task', task_item)
			task_ins = task[task_cls](tool_name, prefLabel=locstr(en_str.replace('Tool', ''), lang='en'))
			tool.usedByTask.append(task_ins)
			task_ins.hasProcessingTool.append(tool)


for d in jdata:
	name = re.sub("^Tool [0-9: ]*", '', d['name']).strip()
	name = OWLUtils.toolname_underline(name)
	tool = SagaTool(name, prefLabel=locstr(d['name'], lang='en'))
	tool.isToolOfSoftware.append(soft.SAGA_GIS)
	for key, value in d.items():
		if type(value) is str:
			string_value(key, value)
		if key == 'command':
			_exe = value['exec']
			if _exe is not None:
				_exe = _exe.replace('saga_cmd ', '')
			tool.hasExecutable = _exe
			tool.hasUsage.append(value['cmd_line'])
		elif key == 'keywords':
			for w in value:
				tool.hasKeyword.append(w)
		elif key == 'comment':
			tool.comment.append(' '.join(value))
		elif key == 'parameter' and value is not None:
			for item, itemValue in value.items():
				if item == 'inputs':
					handle_inout(itemValue, 'input')
				elif item == 'outputs':
					handle_inout(itemValue, 'output')
				elif item == 'options':
					for optionItem in itemValue:
						handle_options(optionItem)
	# task
	handle_task(name, d['name'], d['keywords'])

onto.save(file='saga_test.owl', format="rdfxml")
# update task ontology
task.save()
print('Done!')
