#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/6/10 21:10

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

module_uri = 'http://www.egc.org/ont/process/whitebox'
onto = get_ontology(module_uri)
onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')
import datetime

onto.metadata.created.append(datetime.datetime.today())
onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('WhiteboxTools')
onto.metadata.versionInfo.append('0.12')

with onto:
	class WhiteboxTool(gb.GeoprocessingFunctionality):
		pass


	class WhiteboxInput(cyber.Input):
		pass


	class WhiteboxOutput(cyber.Output):
		pass


	class WhiteboxOption(cyber.Option):
		pass


def param_type(des):
	if re.match("(^Input )", des) is not None:
		return 1
	# 有些输入数据包含Input,如 "D8 pointer uses the ESRI style scheme"
	elif des == "D8 pointer uses the ESRI style scheme":
		return 1
	elif re.match("(^Output )", des) is not None:
		return 2
	elif re.match("(^Optional input )", des) is not None:
		return 3
	else:
		# option
		return 4


def file_type(flag, cmd):
	flag_file = re.search('(' + flag + '=[a-z.A-Z0-9]+ )', cmd)
	if flag_file is None: return None
	fformat = flag_file.group()
	if fformat == '.tif' or fformat == '.dtifep':
		return [data.GeoTIFF, data.GRASS, data.Idrisi_Raster, data.SAGA, data.SAGA_GRID, data.Surfer7, data.Whitebox_GAT_raster]
	elif fformat == '.shp':
		return [data.ESRI_Shapefile]
	elif fformat == '.txt':
		return [data.text_file]
	else:
		return None


def handle_parameter(tool, param):
	# p = None
	dformat = file_type(param['flag'], tool.commandLine[0])
	ptype = param_type(param['description'])
	if 'flag_long' in param.keys():
		pname = param['flag_long'].replace('--', '')
	else:
		pname = param['flag'].replace('--', '')
	_name =  Preprocessor.io_name(pname, onto)
	if ptype == 1:
		p = WhiteboxInput(_name, prefLabel=locstr(pname, lang='en'))
		# p = OTBInput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.input.append(p)
		p.isInput = True
		OWLUtils.link_to_domain_concept(p, pname.replace('_', ' '))
	elif ptype == 2:
		p = WhiteboxOutput(_name, prefLabel=locstr(pname, lang='en'))
		# p = OTBOutput(0, prefLabel=locstr(param['parameter_name'], lang='en'))
		tool.output.append(p)
		p.isOutput = True
		OWLUtils.link_to_domain_concept(p, pname.replace('_', ' '))
	elif ptype == 3:
		p = WhiteboxOption(_name, prefLabel=locstr(pname, lang='en'))
		tool.option.append(p)
		p.isOptional = True
		OWLUtils.link_to_domain_concept(p, pname.replace('_', ' '))
	else:
		p = WhiteboxOption(_name, prefLabel=locstr(pname, lang='en'))
		tool.option.append(p)
		avaliable_choices(p, param['description'])
	if dformat:
		p.supportsDataFormat = dformat
	p.identifier = pname
	p.flag = param['flag']
	if 'flag_long' in param.keys():
		p.longFlag.append(param['flag_long'])
	p.description.append(locstr(param['description'], lang='en'))


def avaliable_choices(option, option_des):
	if "one of" in option_des:
		values = re.findall("\\u2018[a-zA-Z]+\\u2019", option_des)
		if values: option.alternatives = values
		defaultVal = re.findall("\\u2018[a-zA-Z]+\\u2019 \(default\)", option_des)
		if defaultVal: option.defaultValue = defaultVal[0].replace("(default)", '').strip()
	return option


def handle_task(tool, category, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	if re.match("(^GIS Analysis )", category):
		category = 'GIS Analysis'
	elif re.match("(^Image Processing Tools )", category):
		category = 'Image Processing Tools'
	task_cls = config.get('task', category)
	i_task_name = task_name.replace(' ', '_')
	if not task[i_task_name + "_task"]:
		task_ins = task[task_cls](i_task_name + "_task", prefLabel=locstr(task_name + " task", lang='en'))
		task_ins.isAtomicTask = True
		task_ins.identifier = i_task_name
	else:
		task_ins = task[i_task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.processingTool) is False:
		task_ins.processingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def tool_class(category):
	# GIS Analysis => Distance Tools
	if re.match("(^GIS Analysis )", category):
		category = category.replace('GIS Analysis', '').strip()
		return OWLUtils.create_onto_class(onto, category.replace(' ', ''), onto['GISAnalysis'])
	if re.match("(^Image Processing Tools )", category):
		category = category.replace('Image Processing Tools', '').strip()
		return OWLUtils.create_onto_class(onto, category.replace(' ', ''), onto['ImageProcessingTools'])
	if category == 'Math and Stats Tools':
		category = "Math And Stats Tools"
	tool_cls = category.replace(' ', '')
	return OWLUtils.create_onto_class(onto, tool_cls, WhiteboxTool)


def map_to_owl(json_data):
	for d in json_data:
		toolClass = tool_class(d['category'])
		name = Preprocessor.toolname_underline(d['title'])
		tool = toolClass(name, prefLabel=locstr(d['title'], lang='en'))
		tool.isToolOfSoftware.append(cyber.Whitebox_Tools)
		tool.identifier = name
		tool.manualPageURL.append('https://github.com/jblindsay/whitebox-tools/blob/master/manual/WhiteboxToolsManual.md')
		tool.executable = 'whitebox_tools'
		tool.commandLine.append(d['parameter_commandline'][0])
		tool.description.append(locstr(d['description'], lang='en'))

		keywords = OWLUtils.to_keywords(d['description'])
		keywords.extend(d['title'].split(" "))
		OWLUtils.link_to_domain_concept(tool, keywords)

		handle_task(tool, d['category'], d['title'], d['description'])
		OWLUtils.application_category(tool, [], d['category'].replace(' Tools', ''), [])
		for parameter in d['parameter']:
			handle_parameter(tool, parameter)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/whitebox0703.json', 'r') as f:
		jdata = json.load(f)  # list
	# print(len(jdata))
	# otherwise will report stack overflow exception
	size = 1024 * 1024  # related to system
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='whitebox.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('whitebox Done!')
