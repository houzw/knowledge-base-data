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
onto, gb, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class SagaTool(gb.ProcessingTool):
		pass


	class SagaInput(gb.InputData):
		pass


	class SagaOutput(gb.OutputData):
		pass


	class SagaOption(gb.Option):
		pass


	# class SagaConstraint(cyber.Constraint):
	# 	pass

	class SagaAvailableChoice(gb.AvailableChoice):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/saga.json', 'r') as f:
	jdata = json.load(f)  # list

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('SAGA GIS Tools')
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
	_prop = OWLUtils.get_option(config, 'saga', option)
	if _prop is None:
		if onto.__getattr__('has' + option.capitalize()) is None:
			OWLUtils.create_onto_class(onto, 'has' + option.capitalize(), prop_type)
		return 'has' + option.capitalize()
	else:
		return _prop


def get_format(option):
	"""对应的数据格式"""
	config = OWLUtils.get_config(module_path + '/config.ini')
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
			param = SagaInput(0, prefLabel=locstr(io_name, lang='en'))
			# param =SagaInput('input_'+localname, prefLabel=locstr(io_name, lang='en'))
			tool.hasInputData.append(param)
		else:
			param = SagaOutput(0, prefLabel=locstr(io_name, lang='en'))
			# param =SagaOutput('output_'+localname, prefLabel=locstr(io_name, lang='en'))
			tool.hasOutputData.append(param)
		for k, v in ioD.items():
			if k == 'type' and v:
				vr = re.match("[a-zA-Z ]+ (?=\([a-zA-Z ]+\))?", v)
				# print(v)
				dformat = vr.group().strip()
				# print(dformat)
				if not get_format(dformat):
					continue
				# print(data[get_format(dformat)])
				param.supportsDataFormat.append(data[get_format(dformat)])
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
	op = SagaOption(0, prefLabel=locstr(name, lang='en'))
	tool.hasOption.append(op)
	for k, v in option.items():
		if k == "constraints" and v is not None:
			# constraint = SagaConstraint(0,prefLabel=locstr(option['name'], lang='en'))
			# indi.hasConstraint.append(constraint)
			for itemK, itemV in v.items():
				# functional 属性不能使用append
				if itemK == 'availableChoices':
					for choice in itemV:
						availableChoices = SagaAvailableChoice(0, prefLabel=locstr(op_name + ' available choice', lang='en'))
						availableChoices.hasChoice.append(choice['choice'])
						if choice['description'] is not None and (choice['description'] != ' ' or choice['description'] != '-'):
							availableChoices.description.append(choice['description'].strip())
						op.hasAvailableChoice.append(availableChoices)
				else:
					p = get_property(itemK, DataProperty)
					# constraint.__getattr__(p)会返回 str,float,bool等类型？
					# 不能使用 append
					try:
						if option['type'] == 'Floating point':
							op.__getattr__(p).append(float(itemV))
						else:
							op.__getattr__(p).append(itemV)
					except AttributeError:
						if option['type'] == 'Floating point':
							op.__setattr__(p, float(itemV))
						else:
							op.__setattr__(p, itemV)
		elif k == "description" and v == "-":
			continue
		elif type(v) is str:
			v = OWLUtils.name_underline(v)
			p = get_property(k, DataProperty)
			op.__getattr__(p).append(v)


def handle_task(tool_name, en_str, keywords, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in keywords:
			task_cls = config.get('task', task_item)
			if task[tool_name + "_task"] is None:
				task_ins = task[task_cls](tool_name + "_task", prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				# print(des)
				task_ins.description.append(locstr(des, lang='en'))
			# tool.usedByTask.append(task_ins)
			# task_ins.hasProcessingTool.append(tool)
			else:
				task_ins = task[tool_name + "_task"]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.hasProcessingTool) is False:
				task_ins.hasProcessingTool.append(tool)


for d in jdata:
	name = re.sub("^Tool [0-9: ]*", '', d['name']).strip()
	name = OWLUtils.toolname_underline(name)
	tool = SagaTool(name, prefLabel=locstr(d['name'], lang='en'))
	tool.isToolOfSoftware.append(gb.SAGA_GIS)
	tool.hasIdentifier = name
	# task
	des = ' '.join(d['comment'])
	handle_task(name, d['name'], d['keywords'], des)
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
			tool.hasKeywords.append(', '.join(value))
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

onto.save(file='saga.owl', format="rdfxml")
# update task ontology
task.save()
print('SAGA Done!')
