#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/9/14

from owlready2 import *
import json
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

module_uri = 'http://www.egc.org/ont/process/gdal'
onto = get_ontology(module_uri)
onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')
import datetime

onto.metadata.created.append(datetime.datetime.today())
onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('GDAL/OGR')
onto.metadata.versionInfo.append('3.0.1')

with onto:
	class GDALTool(gb.GeoprocessingFunctionality):
		pass


	class GDALInput(cyber.Input):
		pass


	class GDALOutput(cyber.Output):
		pass


	class GDALOption(cyber.Option):
		pass


	class GDALAvailableChoice(cyber.AvailableChoice):
		pass

common_options = ['format', 'formats', 'optfile', 'config', 'debug']

def handle_parameter(tool, param):
	pname = param['name']
	p = None
	_name = Preprocessor.io_name(pname, onto, common_options)
	if 'isInputFile' in param.keys():
		p = GDALInput(_name, prefLabel=locstr(pname, lang='en'))
		p.isInput = True
		tool.input.append(p)
		OWLUtils.link_to_domain_concept(p, pname.replace('_', ' '))
	elif "isOutputFile" in param.keys():
		p = GDALOutput(_name, prefLabel=locstr(pname, lang='en'))
		p.isOutput = True
		tool.output.append(p)
		OWLUtils.link_to_domain_concept(p, pname.replace('_', ' '))
	p.identifier = pname
	if param['flag']: p.flag = param['flag']
	p.isOptional = param['isOptional']
	p.description.append(locstr(param['explanation'], lang='en'))
	p.datatype.append(OWLUtils.get_datatype_iris(param['dataType']))


def handle_options(tool, param, _onto):
	pname = param['name']
	_name = Preprocessor.io_name(pname, _onto, common_options)
	p = GDALOption(_name, prefLabel=locstr(pname, lang='en'))
	p.identifier = pname
	if param['flag']: p.flag = param['flag']
	p.isOptional = param['isOptional']
	p.description.append(locstr(param['explanation'], lang='en'))
	p.datatype.append(OWLUtils.get_datatype_iris(param['dataType']))
	if "available_values" in param.keys():
		for value in param['available_values']:
			p.availableValue.append(value)
		onto, _list = OWLUtils.resources_2_rdf_list(_onto, param['available_values'])
		p.availableList.append(_list)
	if "available_choices" in param.keys():
		p, onto = OWLUtils.handle_choices(p, pname, param['available_choices'], GDALAvailableChoice, _onto)
	if "input_pattern" in param.keys():
		p.inputPattern.append(param['input_pattern'])
	tool.option.append(p)


def handle_task(tool, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	category = tool_class(task_name)
	task_cls = config.get('task', category.name)
	task_name = Preprocessor.space_2_underline(task_name.replace(".py", ""))
	if not task[task_name + "_task"]:
		task_ins = task[task_cls](task_name + "_task", prefLabel=locstr(task_name + " task", lang='en'))
		task_ins.isAtomicTask = True
		task_ins.identifier = task_name
	else:
		task_ins = task[task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.processingTool) is False:
		task_ins.processingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def tool_class(name):
	if str(name).startswith('gnm'):
		tool_cls = "GeographicNetworkPrograms"
	elif str(name).startswith('ogr'):
		tool_cls = "VectorPrograms"
	elif str(name).startswith('gdalmd'):
		tool_cls = "MultidimensionalRasterPrograms"
	else:
		tool_cls = "RasterPrograms"
	return OWLUtils.create_onto_class(onto, tool_cls, GDALTool)


def map_to_owl(json_data):
	for d in json_data:
		name = d['name']
		toolClass = tool_class(name)
		name = Preprocessor.space_2_underline(name)
		tool = toolClass(name, prefLabel=locstr(name, lang='en'))
		tool.isToolOfSoftware.append(cyber.GDAL)
		tool.identifier = name
		tool.definition = d['summary']
		tool.manualPageURL.append(d['manual_url'])
		tool.executable = d['exec']
		tool.commandLine.append(d['syntax'])
		tool.description.append(locstr(d['description'], lang='en'))
		OWLUtils.application_category(tool, [], ['GIS Analysis'], [str(toolClass.name).replace('Programs', '')])
		keywords = OWLUtils.to_keywords(d['description'])
		OWLUtils.link_to_domain_concept(tool, keywords)
		for example in d['example']:
			tool.example.append(example)
		handle_task(tool, d['name'], d['description'])
		for parameter in d['parameters']:
			handle_parameter(tool, parameter)
		for option in d['options']:
			handle_options(tool, option, onto)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/gdal_edited.json', 'r') as f:
		jdata = json.load(f)  # list
	# otherwise will report stack overflow exception
	size = 1024 * 1024  # related to system
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='gdal.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('gdal Done!')
