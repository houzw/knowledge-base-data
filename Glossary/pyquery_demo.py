#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/6/20 9:43
# seeAlso: https://pythonhosted.org/pyquery/
# seeAlso: https://www.cnblogs.com/zhaof/p/6935473.html

from pyquery import PyQuery as pq
from lxml import etree

# import urllib3

# 用 lxml 的 etree 处理一下代码，这样如果 HTML 代码出现一些不完整或者疏漏，
# 都会自动转化为完整清晰结构的 HTML代码。
html_doc = etree.fromstring("<html></html>")

# d is like the $ in jquery
d_doc = pq(html_doc)
'''
d = pq(url="http://www.opengeospatial.org/ogc/glossary/a")
dls = d(".field-item.even>dl").items()
for i in dls:
    word = i("dt").text()
    source = i("dd:first").text()
    definition = i("dd:last").text()

# 打印a-z
import string
for word in string.ascii_lowercase:
    print(word)
'''

html = "<p><strong>ArcGlobe</strong>: <em>[software]</em> ArcGlobe is " \
       "a global three-dimensional visualization and " \
       "analysis environment as part of the Esri ArcGIS suite (3D analyst)," \
       " specializing in global datasets and larger study :areas.</p>"
doc = pq(html)
# print(doc.text())  # 全部文字
# print(doc.html())  # 内部内容，包含子元素标签
print(doc.find('strong').text())
print(doc.find('em').text())
p_strong = doc('em').remove()  # 被移除的内容，doc 被改变
p_clean = doc("strong").remove()
print(doc.text())
print(doc.text().replace(":", "", 1))  # 替换第一个：
