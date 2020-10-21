#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/8/11 20:28
from owlready2 import *
from os import path
from pprint import pprint
import re
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

onto_path.append(path.normpath(path.dirname(__file__)) + '/')
gcmd = get_ontology('/gcmd.owl').load(only_local=True)
skos = get_ontology('/skos.rdf').load(only_local=True)
dc = get_ontology('/dcterms.rdf').load(only_local=True)
gcmd.imported_ontologies.append(skos)
gcmd.imported_ontologies.append(dc)

gcmd.metadata.title.append("Global Change Master Directory keywords")
gcmd.metadata.source.append("https://gcmdservices.gsfc.nasa.gov/static/kms_save/")


def clean(_preflabel):
	oldlabel = re.sub("\([a-z/.,A-Z0-9 ]+\)", '', _preflabel[0]).lower().strip()
	altLabels = []
	if '>' in oldlabel:
		oldlabel = oldlabel.replace('>', 'grater_than')
	elif '<' in oldlabel:
		oldlabel = oldlabel.replace('<', 'less_than')
	if '/' in oldlabel:
		allLabels = oldlabel.split('/')
		newlabel = allLabels[-1:][0]
		# too many items
		exclude = ['nasa','doi','doc','usda','ca','epa','jp','epa','doe','uwa','r','eu','de','dhhs','dmsp']
		if newlabel in exclude:
			newlabel = oldlabel.replace('/', '_')
		altLabels = allLabels[0:-1]
	else:
		newlabel = oldlabel
	newlabel = Preprocessor.replace_2_underline('[ -_]+',newlabel).strip()#newlabel.replace(' - ', '_').replace(' ', '_')
	print(newlabel)
	return newlabel, altLabels


def rename(obj_list, _onto):
	obj_list = list(set(obj_list))
	for o in obj_list:
		preflabel = o.prefLabel
		o.identifier = o.name
		if len(preflabel) > 0:
			# if preflabel[0] == 'NOT APPLICABLE':
			# 	continue
			newlabel, altLabels = clean(preflabel)
			# 只能使用 * ，不能使用正则
			# check duplicate
			rs = _onto.search(iri='https://gcmdservices.gsfc.nasa.gov/kms/concept/' + newlabel + '*')
			# print(rs)
			if len(rs) > 0:
				i = 0
				for r in rs:
					# d means duplicate
					match = re.match(newlabel + "_[0-9]{2,4}$", r.name)
					# if duplicate, append a number
					if r.name == newlabel:
						i += 1
						# print('==: ' + r.name)
					# if more than 1
					elif match is not None:
						# i = int(match.group().rsplit('_', maxsplit=1)[1]) + 1
						i += 1
						# print('match: ' + r.name)
				# print(i)
				if 0 < i < 10:
					newlabel = newlabel + '_0' + str(i)
				elif i > 9:
					newlabel = newlabel + '_' + str(i)

			re.sub("[().]+", '', newlabel)

			o.name = newlabel
			if len(altLabels) > 0:
				for altLabel in altLabels:
					o.altLabel.append(locstr(altLabel, lang='en'))


if __name__ == '__main__':
	# rename(gcmd.classes(), gcmd)
	classes = gcmd.classes()
	for c in classes:
		print(c.name)
		# default belong to skos.Concept
		# otherwise, it will rename twice
		if c.name == 'Concept':
			threading.stack_size(400000)
			thread = threading.Thread(target=rename(c.instances(), gcmd))
			thread.start()
	gcmd.save('gcmd_keywords2.owl')
