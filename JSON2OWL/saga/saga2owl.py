#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/3 16:04

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

module_uri = 'http://www.egc.org/ont/process/saga'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

# sh:declare
# TODO TEST
# OWLUtils.declear_prefix('ns_saga', onto)

with onto:
	# print(gb.GeoprocessingFunctionality)


	class SagaTool(gb.GeoprocessingFunctionality):
		pass


	class SagaInput(gb.InputData):
		pass


	class SagaOutput(gb.OutputData):
		pass


	class SagaOption(gb.Option):
		pass


	class SagaConstraint(gb.Constraint):
		pass


	class SagaAvailableChoice(gb.AvailableChoice):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('SAGA GIS')
onto.metadata.versionInfo.append('7.3.0')
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
		if onto.__getattr__(option) is None:
			OWLUtils.create_onto_class(onto, option, prop_type)
		return option
	else:
		return _prop


def get_format(option):
	"""对应的数据格式"""
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'format', option)
	return _prop


def handle_inout(tool, item_value, in_or_out):
	for ioD in item_value:
		# print(ioD)
		io_name = ioD['name']
		if io_name is None:
			io_name = in_or_out
		if in_or_out == 'input':
			param = SagaInput(prefLabel=locstr(io_name, lang='en'))
			# param = SagaInput(0,prefLabel=locstr(io_name, lang='en')) # blank node prefix with _:
			tool.inputData.append(param)
			param.isInputFile = True
		else:
			param = SagaOutput(prefLabel=locstr(io_name, lang='en'))
			# param =SagaOutput(0, prefLabel=locstr(io_name, lang='en'))
			tool.outputData.append(param)
			param.isOutputFile = True
		if ioD['dataType']:
			vr = re.match("[a-zA-Z ]+ (?=\([a-zA-Z ]+\))?", ioD['dataType'])
			dformat = vr.group().strip()
			if not get_format(dformat):
				continue
			param.supportsDataFormat.append(data[get_format(dformat)])
		param.parameterName = ioD['name']
		param.description.append(ioD['description'])
		param.flag = ioD['flag']
		param.isOptional = ioD['isOptional']


def handle_options(tool, option,_onto):
	op_name = option['name']
	if op_name is None:
		op_name = 'option'
	op = SagaOption(prefLabel=locstr(op_name, lang='en'))
	tool.option.append(op)
	if option['description'] != '-':
		op.description = option['description']
	op.flag = option['flag']
	op.parameterName = Preprocessor.name_underline(op_name)
	constraints = option['constraints']

	if constraints:
		if 'fields_des' in constraints.keys() and constraints['fields_des']:
			op.description.append(constraints['fields_des'])
		else:
			# sc = SagaConstraint(comment=locstr("shacl data constraint", lang='en'))
			sc = SagaConstraint(0, comment=locstr("shacl data constraint", lang='en'))
			if 'parameters_des' in constraints.keys() and constraints['parameters_des']:
				sc.description.append(constraints['parameters_des'])
			op.constraint.append(sc)
			# shacl constraints
			op.property.append(sc)
			if 'minimum' in constraints.keys() and constraints['minimum']:
				sc.minInclusive = constraints['minimum']
				op.minimum = constraints['minimum']  # not shacl
			if 'defaultValue' in constraints.keys() and constraints['defaultValue']:
				sc.defaultValue = constraints['defaultValue']
				op.defaultValue = constraints['defaultValue']  # not shacl
				sc.datatype.append(OWLUtils.get_datatype_iris(option['dataType']))
			if 'maximum' in constraints.keys() and constraints['maximum']:
				sc.maxInclusive = constraints['maximum']
				sc.xmls_maxinclusive = constraints['maximum']
				op.maximum = constraints['defaultValue']  # not shacl
			op.datatypeInString.append(option['dataType'])
			if 'availableChoices' in constraints.keys() and constraints['availableChoices']:
				op, onto = OWLUtils.handle_choices(op, op_name, constraints['availableChoices'], SagaAvailableChoice, _onto)


def handle_task(tool, tool_name, en_str, _keywords, desc):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in _keywords:
			task_cls = config.get('task', task_item)
			task_name = Preprocessor.task_name(tool_name)
			if task[task_name] is None:
				task_ins = task[task_cls](task_name, prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				# task_ins = task[task_cls](tool_name + "_task", prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				task_ins.description.append(locstr(desc, lang='en'))
				task_ins.isAtomicTask = True
			else:
				task_ins = task[task_name]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.processingTool) is False:
				task_ins.processingTool.append(tool)


# TODO TEST
def handle_similar_tools(tool, tool_label):
	"""link tools which have the same names"""
	clean_tool_label = Preprocessor.remove_bracket_content(tool_label)
	similars = onto.search(prefLabel=clean_tool_label + '*')
	if len(similars) > 0:
		for similar in similars:
			if clean_tool_label == Preprocessor.remove_bracket_content(similar.prefLabel[0]):
				tool.closeMatch.append(similar)
				similar.closeMatch.append(tool)


def map_to_owl(json_data):
	for d in json_data:
		"""mapping json data to ontology properties"""
		name = Preprocessor.toolname_underline(d['name'])
		name = re.sub("[()-*,/]", " ", name).strip()
		executable = Preprocessor.normalize("saga_cmd ", d['command']['exec'])
		keywords = d['keywords']
		toolClass = tool_class(keywords)
		if onto[name]:
			# if has the same name and executable
			if onto[name].executable == executable:
				onto[name].is_a.append(toolClass)
				continue
			else:
				name = name + '_' + keywords[0].replace(' ', '_')
		tool = toolClass(Preprocessor.space_2_underline(name), prefLabel=locstr(re.sub('^(Tool)[0-9: ]+', '', d['name']), lang='en'))
		tool.isToolOfSoftware.append(cyber.SAGA_GIS)
		tool.identifier = name
		tool.manualPageURL.append(d['manual_url'])
		# task
		handle_task(tool, name, d['name'], keywords, OWLUtils.join_list(d['description']))
		tool.executable = executable
		tool.commandLine.append(Preprocessor.normalize("Usage: ", d['command']['cmd_line']))
		tool.authors.append(OWLUtils.join_keywords(d['authors']))
		for reference in d['references']:
			tool.references.append(reference)
		# keywords
		keywords.append(name.replace('_', ' '))
		# for keyword in keywords:
		# 	tool.subject.append(keyword)
		OWLUtils.link_to_domain_concept(tool, keywords)

		# applicaiton category
		OWLUtils.application_category(tool, [d['keywords'][0]], d['keywords'][1], d['keywords'][2:])

		tool.description.append(OWLUtils.join_list(d['description']))
		if d['parameters']:
			for item, itemValue in d['parameters'].items():
				if item == 'inputs':
					handle_inout(tool, itemValue, 'input')
				elif item == 'outputs':
					handle_inout(tool, itemValue, 'output')
				elif item == 'options':
					for optionItem in itemValue:
						handle_options(tool, optionItem,onto)


def tool_class(keywords):
	tool_cls = keywords[0].replace(' ', '') + 'Tool'
	return OWLUtils.create_onto_class(onto, tool_cls, SagaTool)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/saga.json', 'r') as f:
		jdata = json.load(f)  # list
	# print(len(jdata))
	# otherwise will report stack overflow exception
	size = 1024 * 1024 * 1024 * 15  # related to system
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='saga.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('SAGA Done!')
