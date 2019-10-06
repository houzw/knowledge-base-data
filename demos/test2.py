#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/22 13:36
# s = 'out_raster(Optional)'
# print(s.startswith('out_'))
# import sys
# sys.path.append('F:/demospace/pywps-flask/processes')
#
# import uuid
# print(uuid.uuid1(node=20190410))
# print(uuid.getnode())
# url = 'https://gcmdservices.gsfc.nasa.gov/static/kms/concept/0a009cb2-9883-48d3-8b91-21efb75b4347.rdf'
# filename = url.replace('https://gcmdservices.gsfc.nasa.gov/static/kms/concept/'+'','')
# print(filename)

s = "Direct neighbours - slope and aspect"
import re

r = re.sub("( - )", '-', s)
print(r)

print(re.match('(^Input )', "Input loading raster file"))
print(re.search('(raster file)', "Input loading raster file"))
s2 = ">>./whitebox_tools -r=Aspect -v --wd=\"/path/to/data/\" ^\n--dem=DEM.tif -o=output.tif \n\n"
rr = re.search('(--dem=[a-z.A-Z0-9]+ )', s2)
rs = rr.group().strip()
print(rs)
filetype = re.search("(?!\.)[a-z]+$", rs)
print(filetype)



