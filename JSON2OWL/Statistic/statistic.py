#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/4/27 17:11

from owlready2 import *
import pandas  as pd
from os import path
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
import matplotlib.pyplot as plt
import numpy as np

# staitistics and visualization of GeoProBase
onto_path.append(path.normpath(path.dirname(__file__)) + '/')


def load_ontologies():
	model_uri = 'http://www.egc.org/ont/process/test'
	onto = get_ontology(model_uri)
	onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
	onto, geospatial = OWLUtils.load_geo_vocabl(onto)
	onto, gb, task, data, cyber = OWLUtils.load_common_for_process_tool(onto)
	onto, context = OWLUtils.load_context(onto)
	arcgis = get_ontology('arcgis.owl').load()
	grass = get_ontology('grass.owl').load(only_local=True)
	otb = get_ontology('otb.owl').load(only_local=True)
	saga = get_ontology('saga.owl').load(only_local=True)
	taudem = get_ontology('taudem.owl').load(only_local=True)
	whitebox = get_ontology('whitebox.owl').load(only_local=True)
	print('ontologies loaded')
	return onto, arcgis, grass, saga, otb, taudem, whitebox


## 1: argis/grass/saga/otb/taudem individuals
def count_instances():
	onto, arcgis, grass, saga, otb, taudem, whitebox = load_ontologies()
	all_instances = []
	arcgis_ins = arcgis['ArcGISTool'].instances()
	arcgis_num = len(arcgis_ins)
	all_instances.extend(arcgis_ins)
	arcgis_cls = arcgis['ArcGISTool'].subclasses()

	grass_ins = grass['GrassTool'].instances()
	grass_num = len(grass_ins)
	all_instances.extend(grass_ins)
	grass_cls = grass['GrassTool'].subclasses()

	saga_ins = saga['SagaTool'].instances()
	saga_num = len(saga_ins)
	all_instances.extend(saga_ins)
	saga_cls = saga['SagaTool'].subclasses()

	otb_ins = otb['OTBTool'].instances()
	otb_num = len(otb_ins)
	all_instances.extend(otb_ins)
	otb_cls = otb['OTBTool'].subclasses()

	taudem_ins = taudem['TauDEMAnalysis'].instances()
	taudem_num = len(taudem_ins)
	all_instances.extend(taudem_ins)
	taudem_cls = taudem['TauDEMAnalysis'].subclasses()

	whitebox_ins = whitebox['WhiteboxTool'].instances()
	whitebox_num = len(whitebox_ins)
	all_instances.extend(whitebox_ins)
	# descendants() include itself
	whitebox_cls = whitebox['WhiteboxTool'].descendants()  # subclasses()

	software = ['arcgis', 'grass', 'saga', 'otb', 'taudem', 'whitebox']
	number_of_tools = [arcgis_num, grass_num, saga_num, otb_num, taudem_num, whitebox_num]
	# subclasses() returns a generator object
	# descendants() include itself
	number_of_categories = [len(list(arcgis_cls)), len(list(grass_cls)), len(list(saga_cls)),
	                        len(list(otb_cls)), len(list(taudem_cls)), len(list(whitebox_cls)) - 1]

	individuals = {'software': software, "number_of_tools": number_of_tools}
	categories = {'software': software, "number_of_categories": number_of_categories}
	return individuals, all_instances, categories


def label_bar(x, y):
	for a, b in zip(x, y):
		# a： x 的坐标，b： y的坐标，b + 0.05 表示上移 0.05, 显示 b 的值
		plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)


def draw_figure(individuals):
	# make it easy to change data
	df = pd.DataFrame(individuals)
	# print(df)
	# print(plt.isinteractive())
	df.plot.bar(x='software', y='number_of_tools', align='center', rot=0, color='lightblue')
	x = np.arange(len(individuals['software']))
	y = individuals['number_of_tools']
	label_bar(x, y)
	plt.ylabel('number of tools')  # processes
	hide_xlabel(plt)
	# plt.xlabel()
	plt.margins(0, 0.1)
	plt.legend(['number of tools'])  # processes
	fig = plt.gcf()
	# w,h
	fig.set_size_inches(5.6, 3.6)
	fig.savefig("tools.png", dpi=300, pad_inches=0)


def draw_category_figure(categories):
	# make it easy to change data
	df = pd.DataFrame(categories)
	# print(df)
	# print(plt.isinteractive())
	df.plot.bar(x='software', y='number_of_categories', align='center', rot=0, color='lightgreen')
	x = np.arange(len(categories['software']))
	y = categories['number_of_categories']
	label_bar(x, y)
	plt.ylabel('number of categories')  # processes
	hide_xlabel(plt)
	# plt.xlabel()
	plt.margins(0, 0.1)
	plt.legend(['number of categories'])  # processes
	fig = plt.gcf()
	# w,h
	fig.set_size_inches(5.6, 3.6)
	fig.savefig("categories.png", dpi=300, pad_inches=0)


# plt.show()  # 必须，否则不显示


def hide_xlabel(target_plt):
	ax = target_plt.axes()
	x_axis = ax.axes.get_xaxis()
	x_axis.get_label().set_visible(False)


## 2: tasks subclassse, top 10
exclude_catories = ['']


def tools_information(tools):
	"""
	collect name and description of tools to build a Doc2Vec model in Gensim. Write them into txt file
	Args:
		tools:
	Returns:
	"""
	softwares = []
	subjects = []
	tool_names = []
	tool_descriptions = []
	for tool in tools:
		description = ''
		tool_name = tool.prefLabel[0]
		# soma saga tools do not have description
		if not tool.description:
			description = tool_name
		else:
			description = tool.description[0].replace('\n', ' ')

		if not description:
			description = tool_name
		tool_names.append(tool_name)
		subject = tool.is_a[0]
		subjects.append(subject)
		if len(tool.isToolOfSoftware) == 0:
			print(tool)
			print(tool.isToolOfSoftware)
		software = tool.isToolOfSoftware[0].name
		softwares.append(software)
		tool_descriptions.append(str(description))
	# # label
	# with open('tools_names.txt', 'w') as f:
	# 	f.writelines(all_tool_names)
	# # text
	# with open('tools_descriptions.txt', 'w') as f:
	# 	f.writelines(all_tool_descriptions)

	all_categories = list(set([subject.name for subject in subjects]))
	df_category = pd.DataFrame({"category_name": all_categories}, columns=['category_name'])
	df_category.to_csv('category_name.txt', index=False)

	labeled_descriptions = {"Name": tool_names, "Category": subjects, "Software": softwares, "Description": tool_descriptions}
	df = pd.DataFrame(labeled_descriptions, columns=['Name', "Category", "Software", 'Description'])
	df.to_csv('tool_descriptions.csv', index=False)


if __name__ == '__main__':
	individuals_count, all_tools, all_cls = count_instances()
	draw_figure(individuals_count)
	draw_category_figure(all_cls)
	tools_information(all_tools)
