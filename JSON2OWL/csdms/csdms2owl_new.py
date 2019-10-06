#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/7/18 21:04

from owlready2 import *
import json
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

import datetime

onto = get_ontology('file://GeoSpatialModels.owl').load()
onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, soft, context = OWLUtils.load_common_for_process_tool(onto)
# data source depends on data
onto, datasource = OWLUtils.load_datasource(onto)

print('ontologies imported')

# create an ontology class

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('GeoSpatial Models')

onto.metadata.created.append(datetime.datetime.today())
module_path = os.path.dirname(__file__)


# remove \n in json first

def map_to_owl(json_data):
	for d in json_data:
		name = d['model_name'].replace('^', '')
		domains = d['domain']
		model_type = d['model_type'].strip()
		clazzs = model_classes(domains, model_type)
		model = clazzs[0](Preprocessor.space_2_underline(name), prefLabel=locstr(name, lang='en'))
		for clazz in clazzs[1:]:
			model.is_a.append(clazz)
		if d['known_as']: model.altLabel.append(locstr(d['known_as'], lang='en'))
		model.isPartOf.append(d['part_of'])
		for extent in d['extent']:
			if extent != '':
				if extent in ['Global', 'Continental']:
					extent = extent + '-Scale'
				extent_instance = context.search_one(iri='*' + extent)
				if extent_instance: model.spatialExtent.append(extent_instance)
		# Spatial dimensions
		if d['dimensions'] != "":
			model.spatialDimension = onto.search_one(prefLabel=d['dimensions'])
		# model.discipline = domains
		model.abstract.append(d['description'])
		model.description.append(d['extended_description'])
		model.subject.append(d['keywords'])
		handle_contact(model, d['contact'])
		handle_technique(model, d['technical'])
		handle_iodata(model, d['input'], 1)
		handle_iodata(model, d['output'], 0)
		handle_processes(model, d['process'])
		handle_testing(model, d['testing'])
		handle_component(model, d['component'])
		model.comment = [d['other']['comments']]
		model.modelWebsite = [d['other']['model_web']]
		if d['other']['manual']: model.manual = [d['other']['manual']]
		handle_application(model, d)
		keywords = [word for word in d['keywords'].split(',') if word is not None]
		keywords.extend(domains)
		# print(keywords)
		OWLUtils.link_to_domain_concept(geospatial, model, keywords)


def handle_component(model, info):
	model.hasOpenMICompliant = [info['openmi']]
	model.hasBMICompliant = [info['bmi']]
	model.hasWMTComponent = [info['wmt']]
	model.modelDOI = [info['model_doi']]
	if info['model_version']:
		model.versionInfo = [info['model_version']]
	if info['file_link']:
		model.fileLink = [info['file_link']]
	if info['couple_with']:
		model.canCoupleWith = [info['couple_with']]


def handle_testing(model, testing_info):
	model.calibrationData = [testing_info['calibration_data_description']]
	# model.hasCalibrationDataSets = [testing_info['calibration_data']]
	model.testDataSets = [testing_info['data_description']]
	model.idealTestingData = [testing_info['ideal_test_data']]


def handle_processes(model, process_info):
	model.representedProcesses = [process_info['processes']]
	model.keyPhysicalParameters = [process_info['params_equations']]
	model.lengthScaleAndResolutionConstraints = [process_info['length_scale_resolution']]
	model.timeScaleAndResolutionConstraints = [process_info['time_scale_resolution']]
	model.numericalLimitations = [process_info['limits']]


def handle_publications(model, pubs):
	for item in pubs:
		pub = onto.ModelPublication()
		pub.bibliographicCitation = [item['title']]
		pub.paperYear = [item['year']]
		pub.modelDescribed = [model]
		pub.type = [item['ref_type']]
		model.publication = [pub]


def handle_application(model, data_item):
	"""manual added application info"""
	if "application" in data_item.keys():
		major_categories = data_item['application']['major_category']
		minor_categories = data_item['application']['minor_category']
		if len(major_categories) > 0: model.majorCategory.extend(major_categories)
		if len(minor_categories) > 0: model.minorCategory.extend(minor_categories)


def handle_technique(model, tech_info):
	# soft.base_iri
	soft_iri = 'http://www.egc.org/ont/gis/cyber#'
	for platform in tech_info['platform']:
		if platform == "": continue
		model_os = soft.search_one(iri=soft_iri + Preprocessor.space_2_underline(platform))
		if model_os: model.supportedPlatform.append(model_os)
	for lang in tech_info['program_lang']:
		if lang == "": continue
		model_lang = soft.search_one(iri=soft_iri + Preprocessor.space_2_underline(lang))
		if model_lang: model.programmingLanguage.append(model_lang)
	for code in tech_info['code']:
		if code != '':
			optimizedType = soft.search_one(iri=soft_iri + Preprocessor.space_2_underline(code))
			if optimizedType: model.codeOptimizedType.append(optimizedType)
			if code == 'Multiple Processors':
				model.supportsMultipleProcessors = [True]
	# functional
	model.startYear = tech_info['start_year']
	model.endYear.append(tech_info['end_year'])
	if tech_info['in_develop'] == 'Yes':
		model.inActiveDevelopment = True
	else:
		model.inActiveDevelopment = False
	if tech_info['license']:
		for soft_license in tech_info['license'].split('or'):
			soft_license = Preprocessor.space_2_underline(soft_license)
			if soft_license != "":
				license_type = soft.search_one(iri=soft_iri + soft_license)
				if license_type:
					license_type = soft.License(soft_license, prefLabel=locstr(soft_license, lang='en'))
				model.license = [license_type]
	model.sourceCodeURL.append(tech_info['source_web'])
	model.sourceCsdmsWebAddress.append(tech_info['source_csdms'])
	model.averageRunTime.append(tech_info['run_time'])
	model.memoryRequirements.append(tech_info['memory'])


def handle_contact(model, contact_info):
	contact = onto.ModelContact()
	# foaf
	contact.firstName.append(contact_info['first_name'])
	contact.lastName.append(contact_info['last_name'])
	contact.institute.append(contact_info['institute'])
	contact.postalAddress.append(contact_info['post_address'])
	contact.postcode.append(contact_info['postcode'])
	contact.city.append(contact_info['city'])
	contact.country.append(contact_info['country'])
	contact.email.append(contact_info['email'])
	contact.phoneNumber.append(contact_info['phone'])
	contact.typeOfContact.append(contact_info['type'])
	model.creatorContact.append(contact)


def handle_model_type(model, model_type):
	searched = onto.search_one(prefLabel=model_type)
	if not searched:
		new_type = onto.ModelType(model_type, prefLabel=locstr(model_type, lang='en'))
	else:
		new_type = searched
	model.modelType.append(new_type)


def model_classes(domains, model_type):
	clazzs = []
	for domain in domains:
		domain = domain.replace(' ', '')
		if domain == 'Hydrology': domain = "Hydrological"
		if model_type == 'Tool':
			clazzs.append(OWLUtils.create_onto_class(onto, domain + 'Tool', onto.GeoSpatialTool))
		else:
			clazzs.append(OWLUtils.create_onto_class(onto, domain + 'Model', onto.GeoSpatialModel))
	return clazzs


# TODO
def handle_iodata(model, io_params, io_type):
	if io_type == 1:
		# some information is defined manuallly
		if model.prefLabel[0] == 'SWAT':
			io_data = onto.ModelInputInfo('swat_input_info')
		else:
			io_data = onto.ModelInputInfo()
	else:
		io_data = onto.ModelOutputInfo()
	io_data.inputDescription.append(io_params['params'])
	if io_params['format_other'] != "": io_data.inputDescription.append(io_params['format_other'])

	for io_format in io_params['format']:
		if io_format == '':
			continue
		if io_format.strip() == 'ASCII':
			io_data.supportsDataFormat = [data.ESRI_ASCII]
		elif io_format.strip() == 'Binary':
			io_data.supportsDataFormat = [data.ESRI_Binary]
		else:
			# print(io_format)
			searched = data.search_one(iri='*' + io_format)
			if searched:
				io_data.supportsDataFormat = [data.ESRI_Binary]
	if io_type == 1:
		model.inputDataInfo = [io_data]
	else:
		model.outputDataInfo = [io_data]


def handle_io(model, io_info):
	if io_info['pre_soft_need'] == 'Yes':
		model.describePreprocessingSoft = [io_info['pre_soft_description']]
	if io_info['post_soft_need'] == 'Yes':
		model.describePostprocessingSoft = [io_info['post_soft_description']]
	if io_info['visual_soft_need'] == 'Yes':
		model.describeVisualizationSoft = [io_info['visual_soft']]


if __name__ == "__main__":
	with open(module_path + '/csdms.json', 'r') as f:
		jdata = json.load(f)  # list
	length = len(jdata)
	# otherwise will report stack overflow exception
	size = 1024 * 1024 * 1024 * 5  # 该值与具体的系统相关
	# print(size)
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='geospatial_models.owl', format="rdfxml")
	soft.save()
	print('CSDMS Done!')
