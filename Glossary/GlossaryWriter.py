#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/6/22 22:02

import pandas as pd


class GlossaryWriter(object):
	@staticmethod
	def write_to_excel(glossary, xlsx, columns):
		df = pd.DataFrame(glossary, columns=columns)
		writer = pd.ExcelWriter(xlsx)
		df.to_excel(writer)
		writer.save()
