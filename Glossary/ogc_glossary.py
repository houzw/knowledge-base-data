#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/6/20 14:33

from pyquery import PyQuery as pq
import string
import pandas as pd

ogc_url = "http://www.opengeospatial.org/ogc/glossary/"


def glossary(base_url):
    """循环获取所有的词汇"""
    glossary_list = []
    for letter in string.ascii_lowercase:
        url = base_url + letter
        doc = pq(url=url)  # html内容，pyquery 对象，可以使用类似jquery的选择方法
        dls = doc(".field-item.even>dl").items()  # dl list
        for dl in dls:
            word = dl("dt").text()
            source = dl("dd:first").text()
            definition = dl("dd:last").text()
            # 有个别词汇没有source
            if source == definition:
                source = ""
            vocab = [word, source, definition]
            glossary_list.append(vocab)
    return glossary_list


# 将上述数据导出到excel文件，columns 为列名
df = pd.DataFrame(glossary(ogc_url), columns=['word', 'source', 'definition'])
writer = pd.ExcelWriter("ogc_glossary.xlsx")
df.to_excel(writer, "ogc")
writer.save()
