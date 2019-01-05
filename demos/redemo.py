#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2018/12/18 9:58
import re

v = re.search("Minimum: \d+\.\d+", "Minimum: 0.000000 Default: 1.000000")
v2 = re.search("Default: (\w+|\d+\.\d+)", "Minimum: 0.000000 Default: xxx")
# print(v)
# print(v2)
ac = re.match("Available Choices: [\[\]0-9A-Za-z -]+[Default:]?",
              "Available Choices: [0] Nearest Neighbour "
              "[1] Bilinear Interpolation "
              "[2] Bicubic Spline Interpolation"
              " [3] B-Spline Interpolation Default: 0")
# print(ac.group())
all = re.findall("\[[0-9]\][ a-zA-Z-]+", ac.group().replace("Default:", ''))
# for l in all:
# print(l)
# print(re.search("(?<=\[)[0-9]", l).group())
# print(re.search("[a-zA-Z -]+", l).group())
# print(re.search("(?P<choice>(?<=\[)[0-9])(?P<des>[a-zA-Z -]+)", l))
# http://www.saga-gis.org/saga_tool_doc/7.0.0/shapes_tools_0.html
test = "28 Parameters: - 1. Available Choices: [0] Albers Equal Area " \
       "[1] Azimuthal Equidistant [2] Airy [3] Aitoff [4] Mod. Stererographics of Alaska " \
       "[5] Apian Globular I [6] August Epicycloidal [7] Bacon Globular [8] Bipolar conic of western hemisphere " \
       "[9] Boggs Eumorphic [10] Bonne (Werner lat_1=90) [11] Cassini [12] Central Cylindrical [13] Equal Area Cylindrical" \
       " [14] Chamberlin Trimetric [15] Collignon [16] Craster Parabolic (Putnins P4) [17] Denoyer Semi-Elliptical [18] Eckert I " \
       "[19] Eckert II [20] Eckert III [21] Eckert IV [22] Eckert V [23] Eckert VI [24] Equidistant Cylindrical (Plate Caree) " \
       "[25] Equidistant Conic [26] Euler [27] Extended Transverse Mercator [28] Fahey [29] Foucaut [30] Foucaut Sinusoidal " \
       "[31] Gall (Gall Stereographic) [32] Geocentric [33] Geostationary Satellite View [34] Ginsburg VIII (TsNIIGAiK)"
# http://www.saga-gis.org/saga_tool_doc/7.0.0/grid_tools_20.html
test2 = "3 Fields: - 1. [8 byte floating point number] Value in Grid 1 " \
        "- 2. [8 byte floating point number] Value in Grid 2 " \
        "- 3. [8 byte floating point number] Resulting Value"
# print(re.search("^\d+ Parameters:",test).group())
# print(re.search("^\d+ Fields:",test2))
test3 = "Available Choices: [0] Difference to left neighbour " \
        "[1] Difference to left neighbour (using a while loop) " \
        "[2] Slope gradient to left neighbour [%%] " \
        "[3] Slope gradient to left neighbour [Degree] Default: 0"
# print(re.search("Available Choices: [\[\]\w()% -]+[Default:]?", test3).group())
# print(re.search("Default: [\w\.]+", test3).group())

t = "Menu: Spatial and Geostatistics|Geographically Weighted Regression"
t = t.replace("Menu: ", '')
# print(re.split("\|", t))
name= "Tool 13: Reprojecting a shapes layer"
name = re.sub("^Tool [0-9]+: ",'',name)
print(name)
name2="Measured Points (PC)"
print(re.sub("\([a-zA-Z ]+\)",'',name2))
