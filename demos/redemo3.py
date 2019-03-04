#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/27 15:57
import re

# |-colorinterp {red|green|blue|alpha|gray|undefined},...]
# [-r {nearest,average,gauss,cubic,cubicspline,lanczos,average_mp,average_magphase,mode}]
s = 'gdal_grid [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/ CInt16/CInt32/CFloat32/CFloat64}] [-of format] [-co "NAME=VALUE"] [-zfield field_name] [-z_increase increase_value] [-z_multiply multiply_value] [-a_srs srs_def] [-spat xmin ymin xmax ymax] [-clipsrc <xmin ymin xmax ymax>|WKT|datasource|spat_extent] [-clipsrcsl sl_statement] [-clipsrclayer layer] [-clipsrcwhere expression] [-l layername]* [-where expression] [-sl select_statement] [-txe xmin xmax] [-tye ymin ymax] [-outsize xsize ysize] [-a algorithm[:parameter1=value1]*] [-] <src_datasource> <dst_filename>'
s2 = 'gdalinfo [--help-general] [-json] [-mm] [-stats] [-hist] [-nogcp] [-nomd]' \
     ' [-norat] [-noct] [-nofl] [-checksum] [-proj4]' \
     ' [-listmdd] [-mdd domain|`all`]*' \
     ' [-sd subdataset] [-oo NAME=VALUE]* datasetname'
s3 = 'gdal2tiles.py [-p profile] [-r resampling] [-s srs] [-z zoom] [-e] [-a nodata] [-v] [-q] [-h] [-k] [-n] [-u url] [-w webviewer] [-t title] [-c copyright] [--processes=NB_PROCESSES] [-g googlekey] [-b bingkey] input_file [output_dir]'
s1 = s.replace("Usage: ", '').replace('gdal_contour', '')

def clean(string, tool):
    return string.replace("Usage: ", '').replace(tool, '')

# options
def optional_params( syntax, tool_name):
    synopsis = syntax.replace('Usage: ', '').replace(tool_name, '').strip()
    optional_params = re.search('\[[\[\]a-zA-Z0-9\- {/}<,:>=._`"*|]+\]', synopsis)
    optional_params = optional_params.group().replace('*', '').strip() if optional_params else ''
    print(optional_params)
    return optional_params


def required_params( syntax, tool_name):
    synopsis = syntax.replace('Usage: ', '').replace(tool_name, '').strip()
    required_params = re.sub('\[[\[\]a-zA-Z0-9\- {/}<,:>=._`"*|]+\]', '', synopsis)
    required_params = required_params.replace('*', '').strip() if required_params else ''
    return required_params


choices_match = re.search("\[-ot {[a-z0-9A-Z/_|, ]+}", optional_params(s,'gdal_grid'))
print(choices_match.group())
print(required_params(s,'gdal_grid'))
# alts = re.search("\[-r {[a-z0-9A-Z/_|, ]+}",clean(s,'gdal_grid'))
# print(alts.group())
# choices = re.search('{[a-z0-9A-Z/_|, ]+}',alts.group()).group()
# print(choices)

# re.search("\[-r [\[\]{}a-z0-9A-Z/_|, ]+\.\.\.]",clean(s,'gdal_grid'))
# choices_match = re.search("\[-ot {[a-z0-9A-Z/_|, ]+}\]", s)
# print(choices_match.group())

if '[-v' in s3:
    print('optional')

print('-v, -versose'.split(','))
print('-v'.split(','))

syntax= "gdaladdo [-r {nearest,average,gauss,cubic,cubicspline,lanczos,average_mp,average_magphase,mode}] [-b band]* [-minsize val] [-ro] [-clean] [-oo NAME=VALUE]* [--help-general] filename [levels]"
n = "{nearest,average,gauss,cubic,cubicspline,lanczos,average_mp,average_magphase,mode}"
n2 = "nearest|aa"
print(re.fullmatch("[a-zA-Z]+",n2))
print(n2.split("|"))