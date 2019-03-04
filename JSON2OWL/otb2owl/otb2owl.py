#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/2/20 22:11

# TODO
from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
import datetime

model_uri = 'http://www.egc.org/ont/process/otb'
onto = get_ontology(model_uri)
onto, shacl, skos, dcterms, props = OWLUtils.load_common(onto)
onto, gb, task, data = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class OTBTool(gb.GeoprocessingTool):
		pass


	class OTBInput(gb.InputData):
		pass


	class OTBOutput(gb.OutputData):
		pass


	class OTBConstraint(gb.Constraint):
		pass


	class OTBAvailableChoices(gb.AvailableChoices):
		pass


	class OTBOption(gb.Option):
		pass
module_path = os.path.dirname(__file__)
with open(module_path + '/otb.json', 'r') as f:
	jdata = json.load(f)  # list

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('Orfeo-Toolbox Tools')

onto.metadata.created.append(datetime.datetime.today())


def handle_task(category, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	task_cls = config.get('task', category)
	# avoid duplicate
	i_task_name = task_name.replace(' ', '_')
	if not task[i_task_name + "_task"]:
		task_ins = task[task_cls](i_task_name + "_task", prefLabel=locstr(task_name + " task", lang='en'))
	else:
		task_ins = task[i_task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.hasProcessingTool) is False:
		task_ins.hasProcessingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def get_datatype(k):
	config = OWLUtils.get_config(module_path + '/config.ini')
	_type = OWLUtils.get_option(config, 'datatype', k)
	if _type is None:
		return 'http://www.w3.org/2001/XMLSchema#string'
	else:
		return _type


def handle_parameters(param):
	# 部分parameter不包含isInputFile等属性
	p = None
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = OTBInput(prefLabel=locstr(param['parameter_name'], lang='en'))
		# p = OTBInput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.hasInputData.append(p)
		p.isInputFile = param['isInputFile']
		p.supportsDataFormat.append(data.GeoTIFF)
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = OTBOutput(0, prefLabel=locstr(param['parameter_name'], lang='en'))
		tool.hasOutputData.append(p)
		p.isOutputFile = param['isOutputFile']
		p.supportsDataFormat.append(data.GeoTIFF)
	p.hasFlag.append(param['flag'])
	p.hasParameterName = param['parameter_name']
	if 'data_type' in param.keys() and param['data_type']:
		p.hasDataTypeStr.append(param['data_type'])
	p.description.append(' '.join(param['explanation']))


# p.isOptional = param['isOptional'] # no this information in document

def handle_options(param):
	o = OTBOption(prefLabel=locstr(param['parameter_name'], lang='en'))
	# p = OTBOption(0, prefLabel=locstr(param['parameter_name'], lang='en'))
	tool.hasOption.append(o)
	sc = OTBConstraint(0, comment=locstr("shacl data constraint", lang='en'))
	o.property.append(sc)
	o.hasParameterName = param['parameter_name']
	if 'data_type' in param.keys() and param['data_type']:
		if param['data_type'] == "Choices":
			o.hasDataTypeStr.append('String')
		o.hasDataTypeStr.append(param['data_type'])
		sc.datatype.append(IRIS[get_datatype(param['data_type'])])
	o.description.append(''.join(param['explanation']))
	# p.isOptional = param['isOptional']
	if 'availableChoices' in param.keys() and param['availableChoices']:
		handle_choices(o, param['parameter_name'], param['availableChoices'])


def handle_choices(option_instance, option_name, choices):
	previous_one = None
	for choice in choices:
		availableChoices = OTBAvailableChoices(comment=locstr(option_name + ' available choices', lang='en'))
		# availableChoices = SagaAvailableChoices(0, comment=locstr(option_name + ' available choices', lang='en'))
		if previous_one is not None:
			previous_one.rdf_rest = availableChoices
		availableChoices.rdf_first = choice['choice']
		availableChoices.hasChoice.append(choice['choice'])
		if choice['description']:
			des = ' '.join(choice['description'])
			if des != ' ' or des != '-':
				availableChoices.description.append(des.strip())
		option_instance.hasAvailableChoice.append(availableChoices)
		previous_one = availableChoices
	previous_one.rest = rdf_nil


for d in jdata:
	if d['category'] == 'Deprecated':
		continue
	name_str = d['name']
	tool = OTBTool(name_str, prefLabel=locstr(d['label'], lang='en'))
	tool.isToolOfSoftware.append(gb.OrfeoToolBox)
	tool.hasIdentifier = name_str
	tool.hasManualPageURL.append(d['manual_url'])
	tool.hasExecutable = d['command']
	tool.description.append(locstr(d['description'], lang='en'))
	tool.definition.append(d['definition'])
	if d['authors']:
		tool.hasAuthors.append(d['authors'])
	for ex in d['example']:
		tool.example.append(ex)
	handle_task(d['category'], d['label'], d['description'])
	for parameter in d['parameters']:
		handle_parameters(parameter)
	for option in d['options']:
		handle_options(option)

onto.save(file='otb.owl', format="rdfxml")
# update task ontology
task.save()
print('OTB Done!')
