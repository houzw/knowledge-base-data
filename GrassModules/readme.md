关键词列表：

https://grass.osgeo.org/grass74/manuals/keywords.html
## command line
scrapy crawl grass -o grass.json

scrapy crawl grass

## post-process
- replace g.parse 
{"manual_url": "https://grass.osgeo.org/grass77/manuals/g.parser.html",
 "name": "g.parser", 
 "definition": "- Providesripts.",
  "keywords": ["general", "support", "scripts"],
   "synopsis": "g.parser [-s] [-t] [-n] filename [argument,...] ", 
   "parameters": [{"parameter": "t", "flag": "-t", "explanation": 
   "Print strings for ", "optional": true},
   {"parameter": "s", "flag": "-s", "explanation": "Write optstea script", "optional": true},
   {"parameter": "n", "flag": "-n", "explanation": "Writutput separall character", "optional": true},
   {"parameter": "filename", "flag": "filename", "explanation": "input file", "optional": false}],
    "description": "\n odule provicoa switch such n An option can sys.exit(main())\n ", "see_also": ["g.filename", "g.findfile", "g.tempfile"], "authors": ["Glynn Clements"], "source_code": "https://trac.osgeo.org/grass/browser/grass/trunk/general/g.parser"},

- remove multiple '\n'
- remove d.label in 'see also', leave d.labels
- remove g.cairocomp, m.eigensystem, r.li (a toolset), r.li.daemon, r.average, r.bitpattern
