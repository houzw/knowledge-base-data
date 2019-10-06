#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/5/17 20:14

from gensim.summarization import keywords

test = "Creates an indicator grid (1,0) of upward curved grid cells according to the Peuker and Douglas algorithm.\
 With this tool, the DEM is first smoothed by a kernel with weights at the center, sides, and diagonals. The Peuker and Douglas (1975) method (also explained in Band, 1986), is then used to identify upwardly curving grid cells. This technique flags the entire grid, then examines in a single pass each quadrant of 4 grid cells, and unflags the highest. The remaining flagged cells are deemed 'upwardly curved', and when viewed, resemble a channel network. This proto-channel network generally lacks connectivity and requires thinning, issues that were discussed in detail by Band (1986).\
Band, L. E., (1986), \"Topographic partition of watersheds with digital elevation models, \" Water Resources Research, 22(1): 15-24. \
Peuker, T. K. and D. H. Douglas, (1975), \"Detection of surface-specific points by local parallel processing of discrete terrain elevation data,\" Comput. Graphics Image Process., 4: 375-387. "
test2="Creates buffer polygons around input features to a specified distance."

p = "Input Pit Filled Elevation Grid"
p2 = "Output D8 Flow Direction Grid"
r = keywords(p2,  split=False, lemmatize=True)
print(r)