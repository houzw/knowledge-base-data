#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/16 16:27

import re

s = 'gdal_translate [--help-general]' \
    '[-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/' \
    'CInt16/CInt32/CFloat32/CFloat64}] [-strict]' \
    ' [-of format] [-b band]* [-mask band] [-expand {gray|rgb|rgba}]' \
    '[-outsize xsize[%]|0 ysize[%]|0] [-tr xres yres]' \
    ' [-r {nearest,bilinear,cubic,cubicspline,lanczos,average,mode}]' \
    ' [-unscale] [-scale[_bn] [src_min src_max [dst_min dst_max]]]* [-exponent[_bn] exp_val]*' \
    ' [-srcwin xoff yoff xsize ysize] [-epo] [-eco]' \
    ' [-projwin ulx uly lrx lry] [-projwin_srs srs_def]' \
    ' [-a_srs srs_def] [-a_ullr ulx uly lrx lry] [-a_nodata value]' \
    '[-a_scale value] [-a_offset value]' \
    ' [-gcp pixel line easting northing [elevation]]*' \
    ' |-colorinterp{_bn} {red|green|blue|alpha|gray|undefined}]' \
    ' |-colorinterp {red|green|blue|alpha|gray|undefined},...]' \
    ' [-mo "META-TAG=VALUE"]* [-q] [-sds]' \
    ' [-co "NAME=VALUE"]* [-stats] [-norat]' \
    ' [-oo NAME=VALUE]*' \
    ' src_dataset dst_dataset'
# <src_datasource> <dst_filename>

# clean up
syntax = s.replace('Usage:', '').replace('[OPTIONS]', '').replace('Options:', '')
executable = re.match('^[a-z_]+ ', syntax)
if executable:
	print(str(executable.group()).strip())

# options = re.findall(' \[[-\w ="|{},.]+\](?=[ *]?) ', syntax)
# for option in options:
# 	print(option)
# d = dict()
# d[None] = 'a'
# d['b'] = 'b'
# for k,v in d.items():
#     print(k)
#     print(v)


synopsis = "i.eb.evapfr [-m] netradiation=name soilheatflux=name sensibleheatflux=name evaporativefraction=name  [soilmoisture=name]   [--overwrite]  [--help]  [--verbose]  [--quiet]  [--ui]"
r = re.match('[a-z.]+ ', synopsis)
print('rr')

s2 = "i.eb.evapfr"

print(s2.split('.', maxsplit=1))
import datetime

print(datetime.datetime.today())
ss = "Raster To Video (Conversion)"
ss2 = "Table "
rr = re.match("[a-zA-Z ]+ (?=\([a-zA-Z ]+\))?", ss2)
print(rr)
print(re.search("\([a-zA-Z]+\)", ss2))
print(str('RasterToVideo_conversion').split('_')[0])

ex = {
	"title": "RasterToPolygon example (Python window)",
	"desc": "Converts a raster dataset to polygon features.\r\n",
	"code": "import arcpy from arcpy import env env . workspace = \"C:/data\" arcpy . RasterToPolygon_conversion ( \"zone\" , \"c:/output/zones.shp\" , \"NO_SIMPLIFY\" , \"VALUE\" )"
}
print(str(ex))
print(str(ex).replace('{',''))
tt = 'Geographically Weighted Regression (Spatial Statistics)'
print(re.findall("\([a-zA-Z* ]+\)", tt))
