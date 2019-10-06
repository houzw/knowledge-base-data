#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/24 13:43

"""
extract cf-standard-name-table.xml
"""
from owlready2 import *
from xml.etree import ElementTree as ET
import re
from os import path
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
import datetime

module_path = os.path.dirname(__file__)

onto_path.append(path.normpath(path.dirname(__file__)) + '/')
skos = get_ontology('file://../OwlConvert/skos.rdf').load(only_local=True)
dcterms = get_ontology('file://../OwlConvert/dcterms.rdf').load(only_local=True)
# load predefined ontology schema without individuals
onto = get_ontology('/cf-standard-names.owl').load(only_local=True)
onto.imported_ontologies.append(skos)
onto.imported_ontologies.append(dcterms)
# onto = OWLUtils.load_common(onto)
print('ontologies imported')

with open(module_path + '/cf-standard-name-table.xml', 'r', encoding="utf-8") as file:
	# 将xml文档中内容读取到strXml中
	strXml = file.read()
	# XML将字符串解析成xml特殊对象，返回xml.etree.ElementTree.Element对象，这个是根节点
	root = ET.XML(strXml)
onto.metadata.creator.append('houzhiwei')
onto.metadata.created.append(datetime.datetime.today())

atmosphere_dynamics = 'air_pressure|atmosphere_vorticity|atmosphere_streamfunction|wind|momentum_in|air|gravity_wave|ertel|geopotential|omega|atmosphere_dissipation|atmosphere_energy|atmosphere_drag|atmosphere_stress|surface_stress'
atmospheric_chemistry = 'aerosol|dry_deposition|wet_deposition|production|emission|mole'
carbon_cycle = 'carbon|leaf|vegetation'
cloud = 'cloud'
sea_ice = 'sea_ice'
surface = 'surface'
radiation = 'radiative|longwave|shortwave|brightness|radiance|albedo'
ocean_dynamics = 'ocean_streamfunction|sea_water_velocity|ocean_vorticity'
hydrology = 'atmosphere_water|canopy_water|precipitation|rain|snow|moisture|freshwater|runoff|root|humidity|transpiration|evaporation|water_vapour|river'

for entry in root.iter("entry"):
	indi = None
	name = entry.get('id')
	label = name.replace('_',' ')
	name = name.replace(' ','_')
	if re.search(atmosphere_dynamics, name):
		indi = onto.AtmosphereDynamics(name, prefLabel=locstr(label, lang='en'))
	elif re.search(atmospheric_chemistry, name):
		indi = onto.AtmosphericChemistry(name, prefLabel=locstr(label, lang='en'))
	elif re.search(carbon_cycle, name):
		indi = onto.CarbonCycle(name, prefLabel=locstr(label, lang='en'))
	elif re.search(cloud, name):
		indi = onto.Cloud(name, prefLabel=locstr(label, lang='en'))
	elif re.search(hydrology, name):
		indi = onto.Hydrology(name, prefLabel=locstr(label, lang='en'))
	elif re.search(ocean_dynamics, name):
		indi = onto.OceanDynamics(name, prefLabel=locstr(label, lang='en'))
	elif re.search(radiation, name):
		indi = onto.Radiation(name, prefLabel=locstr(label, lang='en'))
	elif re.search(sea_ice, name):
		indi = onto.SeaIce(name, prefLabel=locstr(label, lang='en'))
	elif re.search(surface, name):
		indi = onto.Surface(name, prefLabel=locstr(label, lang='en'))
	else:
		indi = onto.CFStandardName(name, prefLabel=locstr(label, lang='en'))
	unit = entry.findtext('canonical_units')
	grib = entry.findtext('grib')
	amip = entry.findtext('amip')
	description = entry.findtext('description')
	indi.hasGRIB.append(grib)
	indi.hasCanonicalUnit.append(unit)
	indi.hasAMIP.append(amip)
	indi.description.append(description)


for alias in root.iter("alias"):
	entry_name = alias.findtext('entry_id')
	cls = onto[entry_name].is_a
	alias_name = alias.get('id')
	alias_name = alias_name.replace(' ','_')
	label = alias_name.replace('_',' ')
	alias_indi = cls[0](alias_name, prefLabel=locstr(label, lang='en'))
	# sameAs
	onto[entry_name].equivalent_to.append(alias_indi)

# save created individuals
onto.save()
print('cf Done!')