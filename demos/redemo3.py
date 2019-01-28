#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/27 15:57
import re

# |-colorinterp {red|green|blue|alpha|gray|undefined},...]
# [-r {nearest,average,gauss,cubic,cubicspline,lanczos,average_mp,average_magphase,mode}]
s = 'gdal_grid [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/' \
    'CInt16/CInt32/CFloat32/CFloat64}]' \
    ' [-of format] [-co "NAME=VALUE"]' \
    ' [-r {nearest, average, gauss, cubic, cubicspline, lanczos, average_mp, average_magphase, mode}]' \
    ' [-zfield field_name] [-z_increase increase_value] [-z_multiply multiply_value]' \
    ' [-a_srs srs_def] [-spat xmin ymin xmax ymax]' \
    ' [-clipsrc <xmin ymin xmax ymax>|WKT|datasource|spat_extent]' \
    ' [-clipsrcsql sql_statement] [-clipsrclayer layer]' \
    ' [-clipsrcwhere expression]' \
    ' [-l layername]* [-where expression] [-sql select_statement]' \
    ' [-txe xmin xmax] [-tye ymin ymax] [-outsize xsize ysize]' \
    ' [-a algorithm[:parameter1=value1]*] [-q]' \
    ' <src_datasource> <dst_filename>'
s2 = 'gdalinfo [--help-general] [-json] [-mm] [-stats] [-hist] [-nogcp] [-nomd]' \
     ' [-norat] [-noct] [-nofl] [-checksum] [-proj4]' \
     ' [-listmdd] [-mdd domain|`all`]*' \
     ' [-sd subdataset] [-oo NAME=VALUE]* datasetname'
s1 = s.replace("Usage: ", '').replace('gdal_contour', '')

def clean(string, tool):
    return string.replace("Usage: ", '').replace(tool, '')

# print(s1)
r1 = re.sub('\[[\[\]a-zA-Z0-9\- <>=._`*|]+\]', '', s1).replace('*', '').strip()
print(r1)
# r2 = re.sub('\[[\[\]a-zA-Z0-9\- <>=._`*|]+\]', '', s2)
# print(r2)
r3 = re.search('\[[\[\]a-zA-Z0-9\- <>=._`*|]+\]', s1)
r4 = r3.group()
r5 = re.search('\[-dsco', r4)
print(r5)
print('[-e' in r4)
alts = re.search("\[-r {[a-z0-9A-Z/_|, ]+}",clean(s,'gdal_grid'))
print(alts.group())
choices = re.search('{[a-z0-9A-Z/_|, ]+}',alts.group()).group()
print(choices)

re.search("\[-r [\[\]{}a-z0-9A-Z/_|, ]+\.\.\.]",clean(s,'gdal_grid'))