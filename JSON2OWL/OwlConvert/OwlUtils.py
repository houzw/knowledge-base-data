#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/2 11:33
from owlready2 import *
from configparser import ConfigParser, NoOptionError
from os import path

class OWLUtils(object):

	@staticmethod
	def curr_path(file_path):
		# print('file://' + path.normpath(path.dirname(__file__) + file_path))
		return 'file://' + path.normpath(path.dirname(__file__) + file_path)

	@staticmethod
	def load_common(onto: Ontology):
		"""
		load skos, dcterms and UniProps into target ontology

		Args:
			onto: Ontology which needs to import ontologies like skos

		Returns: Ontology with imported ontologies
		"""
		onto_path.append(path.normpath(path.dirname(__file__)) + '/')
		skos = get_ontology('/skos.rdf').load(only_local=True)
		dcterms = get_ontology('/dcterms.rdf').load(only_local=True)
		props = get_ontology('/UniProps.owl').load(only_local=True)
		onto.imported_ontologies.append(props)
		onto.imported_ontologies.append(skos)
		onto.imported_ontologies.append(dcterms)
		return onto

	@staticmethod
	def load_common_for_process_tool(onto: Ontology):
		onto = OWLUtils.load_common(onto)
		soft = get_ontology('/GeospatialSoftwares.owl').load(only_local=True)
		geoprocessor = get_ontology('/geoprocessors-base.owl').load(only_local=True)
		task = get_ontology('/task.owl').load(only_local=True)
		data = get_ontology('/DataDescription.owl').load(only_local=True)
		onto.imported_ontologies.append(soft)
		onto.imported_ontologies.append(geoprocessor)
		onto.imported_ontologies.append(task)
		onto.imported_ontologies.append(data)
		return onto, soft, geoprocessor, task,data

	@staticmethod
	def create_onto_class(onto: Ontology, name, parent_class):
		with onto:
			clazz = types.new_class(name, (parent_class,))
		return clazz

	@staticmethod
	def get_config(ini):
		"""
		使用自定义的OwlConfigerParser
		Args:
			ini: ini 配置文件

		Returns:

		"""
		config = ConfigParser()
		# 保留大小写不变
		# https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
		config.optionxform = str
		config.read(ini, encoding='utf-8')
		return config

	@staticmethod
	def get_option(config, section, option):
		try:
			return config.get(section, option)
		except NoOptionError:
			return None

	@staticmethod
	def name_underline(name: str):
		name = re.sub("\([a-zA-Z /]+\)", '', name.lower()).strip()
		return name.replace(" ", "_").replace(',', '').replace("(*)", '')

	@staticmethod
	def toolname_underline(name: str):
		return name.lower().strip().replace('(', '').replace(')', '').replace(" ", "_").replace(',', '').replace("(*)", '')
