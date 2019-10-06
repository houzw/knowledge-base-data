#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/6/20 8:30

# merge all process owl files into one: geoprobase
from owlready2 import *
from os import path
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from rdflib import URIRef

model_uri = 'http://www.egc.org/ont/geoprobase#'
onto_path.append(path.normpath(path.dirname(__file__)) + '/')
onto = get_ontology(model_uri)
onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
onto, datasource = OWLUtils.load_datasource(onto)
arcgis = get_ontology('arcgis.owl').load()
gdal = get_ontology('gdal.owl').load(only_local=True)
grass = get_ontology('grass.owl').load(only_local=True)
otb = get_ontology('otb.owl').load(only_local=True)
saga = get_ontology('saga.owl').load(only_local=True)
taudem = get_ontology('taudem.owl').load(only_local=True)
whitebox = get_ontology('whitebox.owl').load(only_local=True)
models = get_ontology('geospatial_models.owl').load(only_local=True)

imports = [skos, data, sh, foaf, props, dcterms, task, cyber, gb, context, datasource,
           models, arcgis, gdal, grass, otb, saga, taudem, whitebox]
for o in imports:
	onto.imported_ontologies.append(o)

# http://owlready.8326.n8.nabble.com/ontology-merging-td425.html
world = default_world
graph = world.as_rdflib_graph()
# 绑定前缀，不然输出 ns+数字 作为前缀
# 参考StackOverflow上的一个回答
graph.bind('geoprobase', URIRef('http://www.egc.org/ont/geoprobase#'))
graph.bind('skos', URIRef('http://www.w3.org/2004/02/skos/core#'))
graph.bind('data', URIRef('http://www.egc.org/ont/data#'))
graph.bind('datasource', URIRef('http://www.egc.org/ont/datasource#'))
graph.bind('model', URIRef('http://www.egc.org/ont/model/geospatial#'))
graph.bind('cyber', URIRef('http://www.egc.org/ont/gis/cyber#'))
graph.bind('props', URIRef('http://www.egc.org/ont/base/props#'))
graph.bind('context', URIRef('http://www.egc.org/ont/context#'))
graph.bind('gcmd', URIRef('https://gcmdservices.gsfc.nasa.gov/kms/concept/'))
graph.bind('kms', URIRef('http://gcmd.gsfc.nasa.gov/kms#'))
graph.bind('taudem', URIRef('http://www.egc.org/ont/process/taudem#'))
graph.bind('gdal', URIRef('http://www.egc.org/ont/process/gdal#'))
graph.bind('whitebox', URIRef('http://www.egc.org/ont/process/whitebox#'))
graph.bind('saga', URIRef('http://www.egc.org/ont/process/saga#'))
graph.bind('arcgis', URIRef('http://www.egc.org/ont/process/arcgis#'))
graph.bind('grass', URIRef('http://www.egc.org/ont/process/grass#'))
graph.bind('otb', URIRef('http://www.egc.org/ont/process/otb#'))
graph.bind('dcterms', URIRef('http://purl.org/dc/terms/'))
graph.bind('cf', URIRef('http://www.egc.org/ont/vocab/cf#'))
graph.bind('dta', URIRef('http://www.egc.org/ont/domain/dta#'))
graph.bind('task', URIRef('http://www.egc.org/ont/context/task#'))
graph.bind('sh', URIRef('http://www.w3.org/ns/shacl#'))
graph.bind('process', URIRef('http://www.egc.org/ont/gis/process#'))
graph.bind('dc', URIRef('http://purl.org/dc/elements/1.1/'))
graph.bind('foaf', URIRef('http://xmlns.com/foaf/0.1/'))
graph.bind('owl', URIRef('http://www.w3.org/2002/07/owl#'))
graph.serialize(destination='geoprobase.owl', format="xml")  # 即rdfxml
# onto.save('geoprobase.nt','ntriples')
alltriples = len(list(graph.triples((None, None, None))))
print(alltriples)  # 648998, 2019-10-03
print('merge done!')
