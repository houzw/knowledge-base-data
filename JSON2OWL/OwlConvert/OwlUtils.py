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
		shacl = get_ontology('/shacl.rdf').load(only_local=True)
		skos = get_ontology('/skos.rdf').load(only_local=True)
		dcterms = get_ontology('/dcterms.rdf').load(only_local=True)
		props = get_ontology('/UniProps.owl').load(only_local=True)
		onto.imported_ontologies.append(shacl)
		onto.imported_ontologies.append(props)
		onto.imported_ontologies.append(skos)
		onto.imported_ontologies.append(dcterms)
		return onto,shacl,skos,dcterms,props

	@staticmethod
	def load_common_for_process_tool(onto: Ontology):
		data = get_ontology('/data.owl').load(only_local=True)
		gb = get_ontology('/gis-base.owl').load(only_local=True)
		task = get_ontology('/task.owl').load(only_local=True)
		onto.imported_ontologies.append(gb)
		onto.imported_ontologies.append(task)
		onto.imported_ontologies.append(data)
		return onto, gb, task, data

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
		name = re.sub("\([a-zA-Z0-9* /]+\)", '', name.lower()).strip()
		name = re.sub("\[[()a-zA-Z0-9*^\- /]+\]", '', name).strip()
		return name.replace(" ", "_").replace(',', '')

	@staticmethod
	def toolname_underline(name: str):
		name = re.sub('[()*&,]','',name.lower().strip())
		name = re.sub('[ /]','_',name)
		name = re.sub('[_]+','_',name)
		return name

	@staticmethod
	def declear_prefix(prefix,onto):
		o = Thing(onto.ontology.base_iri,namespace=onto.get_namespace(onto.ontology.base_iri))
		pre = onto.get_namespace(base_iri='http://www.w3.org/ns/shacl#').PrefixDeclaration(prefix)
		pre.prefix = [prefix]
		pre.namespace = [onto.ontology.base_iri]
		o.declare.append(pre)
