#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/7/10 15:49

# https://www.cnblogs.com/jamespei/p/5339769.html
import codecs
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines, PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextBoxVertical, LTTextLine, LTImage, LTFigure, LTChar, \
	LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

pdf = 'Runoff simulation by SWAT model using high-resolution gridded precipitation in the upper Heihe River Basin, Northeastern Tibetan Plateau.pdf'
pdf2 = 'water-08-00178.pdf'
path = r'./' + pdf2

# 不能完整获取PDF内容


def parse():
	f = codecs.open(path, mode='rb', encoding='ISO-8859-1')  # 二进制
	parser = PDFParser(f)
	doc = PDFDocument()
	# 连接解析器与文档对象
	parser.set_document(doc)
	doc.set_parser(parser)
	doc.initialize()  # 若有密码则提供密码
	if not doc.is_extractable:
		raise PDFTextExtractionNotAllowed
	else:
		manager = PDFResourceManager()
		# 创建一个PDF设备对象
		params = LAParams()
		# 创建一个PDF页面聚合对象
		device = PDFPageAggregator(manager, laparams=params)
		# 解释器
		interpreter = PDFPageInterpreter(manager, device)

		for page in doc.get_pages():
			interpreter.process_page(page)
			layout = device.get_result()
			for x in layout:
				if isinstance(x, LTTextBox):
					with codecs.open(r'./test1.txt', mode='a', encoding='ISO-8859-1') as f:
						result = x.get_text()
						print(result)
						f.write(result + '\n')
				elif isinstance(x, LTTextBoxHorizontal):
					with codecs.open(r'./test2.txt', mode='a', encoding='ISO-8859-1') as f2:
						result2 = x.get_text()
						print(result2)
						f2.write(result2 + '\n')
				elif isinstance(x, LTTextLine):
					with codecs.open(r'./test3.txt', mode='a', encoding='ISO-8859-1') as f3:
						result3 = x.get_text()
						print(result3)
						f3.write(result3 + '\n')


if __name__ == "__main__":
	parse()
