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
onto, sh, skos, dcterms, props = OWLUtils.load_common(onto)
onto, gb, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

# sh:declare
# TODO TEST
OWLUtils.declear_prefix('ns_saga', onto)

with onto:
	class SagaTool(gb.GeoprocessingTool):
		pass


	class SagaInput(gb.InputData):
		pass


	class SagaOutput(gb.OutputData):
		pass


	class SagaOption(gb.Option):
		pass


	class SagaConstraint(gb.Constraint):
		pass


	class SagaAvailableChoices(gb.AvailableChoices):
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


# def string_value(str_key, str_value):
# 	s_prop = get_property(str_key, DataProperty)
# 	if not str_value or str_value == '' or str_value == '-':
# 		pass
# 	else:
# 		if tool.__getattr__(s_prop) is None:
# 			tool.__setattr__(s_prop, str_value)
# 		else:tool.__getattr__(s_prop).append(str_value)

def handle_inout(item_value, in_or_out):
	for ioD in item_value:
		# print(ioD)
		io_name = ioD['name']
		if io_name is None:
			io_name = in_or_out
		if in_or_out == 'input':
			param = SagaInput(prefLabel=locstr(io_name, lang='en'))
			# param = SagaInput(0,prefLabel=locstr(io_name, lang='en')) # blank node prefix with _:
			tool.hasInputData.append(param)
			param.isInputFile = True
		else:
			param = SagaOutput(prefLabel=locstr(io_name, lang='en'))
			# param =SagaOutput(0, prefLabel=locstr(io_name, lang='en'))
			tool.hasOutputData.append(param)
			param.isOutputFile = True
		if ioD['type']:
			vr = re.match("[a-zA-Z ]+ (?=\([a-zA-Z ]+\))?", ioD['type'])
			dformat = vr.group().strip()
			if not get_format(dformat):
				continue
			param.supportsDataFormat.append(data[get_format(dformat)])
		param.hasParameterName = ioD['name']
		param.description.append(ioD['description'])
		param.hasFlag.append(ioD['identifier'])
		param.isOptional = ioD['optional']


def handle_options(option):
	op_name = option['name']
	if op_name is None:
		op_name = 'option'
	op = SagaOption(prefLabel=locstr(op_name, lang='en'))
	tool.hasOption.append(op)
	if option['description'] != '-':
		op.description = option['description']
	op.hasFlag.append(option['identifier'])
	op.hasParameterName = OWLUtils.name_underline(op_name)
	constraints = option['constraints']

	if constraints:
		if 'fields_des' in constraints.keys() and constraints['fields_des']:
			op.description.append(constraints['fields_des'])
		else:
			sc = SagaConstraint(comment=locstr("shacl data constraint", lang='en'))
			# sc = SagaConstraint(0,comment=locstr("shacl data constraint", lang='en'))
			if 'parameters_des' in constraints.keys() and constraints['parameters_des']:
				sc.description.append(constraints['parameters_des'])
			op.hasConstraint.append(sc)
			# shacl constraints
			op.property.append(sc)
			if 'minimum' in constraints.keys() and constraints['minimum']:
				sc.minInclusive = constraints['minimum']
				op.hasMinimum = constraints['minimum']  # not shacl
			if 'default' in constraints.keys() and constraints['default']:
				sc.defaultValue = constraints['default']
				op.hasDefaultValue = constraints['default']  # not shacl
				if option['type'] == 'Floating point':
					sc.datatype.append(IRIS['http://www.w3.org/2001/XMLSchema#float'])
				elif option['type'] == 'Boolean':
					sc.datatype.append(IRIS['http://www.w3.org/2001/XMLSchema#boolean'])
				elif option['type'] == 'Integer':
					sc.datatype.append(IRIS['http://www.w3.org/2001/XMLSchema#integer'])
				else:
					sc.datatype.append(IRIS['http://www.w3.org/2001/XMLSchema#string'])
			if 'maximum' in constraints.keys() and constraints['maximum']:
				sc.maxInclusive = constraints['maximum']
				sc.xmls_maxinclusive = constraints['maximum']
				op.hasMaximum = constraints['default']  # not shacl
			op.hasDataTypeStr.append(option['type'])
			if 'availableChoices' in constraints.keys() and constraints['availableChoices']:
				handle_choices(op, op_name, constraints['availableChoices'])

def handle_task(tool_name, en_str, keywords, desc):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in keywords:
			task_cls = config.get('task', task_item)
			if task[tool_name + "_task"] is None:
				task_ins = task[task_cls](tool_name + "_task", prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				# print(des)
				task_ins.description.append(locstr(desc, lang='en'))
			# tool.usedByTask.append(task_ins)
			# task_ins.hasProcessingTool.append(tool)
			else:
				task_ins = task[tool_name + "_task"]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.hasProcessingTool) is False:
				task_ins.hasProcessingTool.append(tool)


def handle_choices(option_instance, option_name, choices):
	previous_one = None
	for choice in choices:
		availableChoices = SagaAvailableChoices(comment=locstr(option_name + ' available choices', lang='en'))
		# availableChoices = SagaAvailableChoices(0, comment=locstr(option_name + ' available choices', lang='en'))
		# todo test
		if previous_one is not None:
			previous_one.rdf_rest = availableChoices
		availableChoices.rdf_first = choice['choice']
		availableChoices.hasChoice.append(choice['choice'])
		if choice['description'] is not None and (choice['description'] != ' ' or choice['description'] != '-'):
			availableChoices.description.append(choice['description'].strip())
		option_instance.hasAvailableChoice.append(availableChoices)
		previous_one = availableChoices
	previous_one.rest = rdf_nil


for d in jdata:
	name = re.sub("^Tool [0-9: ]*", '', d['name']).strip()
	name = OWLUtils.toolname_underline(name)
	tool = SagaTool(name, prefLabel=locstr(d['name'], lang='en'))
	tool.isToolOfSoftware.append(gb.SAGA_GIS)
	tool.hasIdentifier = name
	tool.hasManualPageURL.append(d['manual_url'])
	# task
	des = ' '.join(d['comment'])
	handle_task(name, d['name'], d['keywords'], des)
	_exe = d['command']['exec']
	if _exe is not None:
		_exe = _exe.replace('saga_cmd ', '')
	tool.hasExecutable = _exe
	tool.hasUsage.append(d['command']['cmd_line'])
	tool.hasKeywords.append(', '.join(d['keywords']))
	tool.comment.append(' '.join(d['comment']))
	if d['parameter']:
		for item, itemValue in d['parameter'].items():
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
