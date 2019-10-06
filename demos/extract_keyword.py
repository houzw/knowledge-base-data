#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/5/14 21:45
# https://php.ctolib.com/rake-nltk.html

from rake_nltk import Rake
from nltk.corpus import stopwords
from string import punctuation

# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake(max_length=5)

test = "Creates an indicator grid (1,0) of upward curved grid cells according to the Peuker and Douglas algorithm.\
 With this tool, the DEM is first smoothed by a kernel with weights at the center, sides, and diagonals. The Peuker and Douglas (1975) method (also explained in Band, 1986), is then used to identify upwardly curving grid cells. This technique flags the entire grid, then examines in a single pass each quadrant of 4 grid cells, and unflags the highest. The remaining flagged cells are deemed 'upwardly curved', and when viewed, resemble a channel network. This proto-channel network generally lacks connectivity and requires thinning, issues that were discussed in detail by Band (1986).\
Band, L. E., (1986), \"Topographic partition of watersheds with digital elevation models, \" Water Resources Research, 22(1): 15-24. \
Peuker, T. K. and D. H. Douglas, (1975), \"Detection of surface-specific points by local parallel processing of discrete terrain elevation data,\" Comput. Graphics Image Process., 4: 375-387. "

# Extraction given the text.
r.extract_keywords_from_text(test)
# r.extract_keywords_from_text("Converts a raster dataset to polygon features.")

# Extraction given the list of strings where each string is a sentence.
# r.extract_keywords_from_sentences(<list of sentences>)

# To get keyword phrases ranked highest to lowest.
print(r.get_ranked_phrases())

# To get keyword phrases ranked highest to lowest with scores.
r.get_ranked_phrases_with_scores()
