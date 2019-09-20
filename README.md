## target
collect data to build knowledge base for intelligent geographic modeling environment

## technology
- Scrapy
- PyQuery
- pandas
- owlready2

## start scrapy
```shell
scrapy startproject xxx
cd xxx
scrapy genspider example example.com
```

## coding
- items
- spiders


## run  Scrapy
- in SWATArticle  directory
  `scrapy crawl swat_article -o articles.csv`
- in CSDMS  directory
  `scrapy crawl csdms -o csdms.json`
  if only need hydrological models，modify start url, and execute
  `scrapy crawl csdms -o hydro.json`
- in TauDEM  directory
  `scrapy crawl taudem -o taudem.json`
- in SAGA  directory
    `scrapy crawl saga -o saga.json`
    > note: change "D Shapes Viewer" to "3D Shapes Viewer";
- in GrassModules directory
    `scrapy crawl grass -o grass.json`
- in ArcGIS directory
    `scrapy crawl arcgis -o arcgis.json`
- in GDAL directory
    `scrapy crawl gdal_spider -o gdal.json`
- in OTB directory
    `scrapy crawl otb -o otb.json`
## mapping to owl
- 去除csv或json中不合法的Unicode字符
- 检查Json文件和文档内容是否匹配
- 检查是否存在 name 属性为 null的，去掉这些对象
- 设计本体模型，包括类的层次结构的组织，属性和关系的设计等
- JSON2OWL下编写转换方法并执行。如
  - csdms2owl.py
  - taudem2owl.py
- 检查修正

> http://www.saga-gis.org/saga_tool_doc/7.1.1/ta_hydrology_1.html 中一段comment内容未能抽取：“Flow routing methods provided by this tool:
    Deterministic 8 (aka D8, O'Callaghan & Mark 1984)
    Rho 8 (Fairfield & Leymarie 1991)
    Multiple Flow Direction (Freeman 1991, Quinn et al. 1991)
    Deterministic Infinity (Tarboton 1997)”

## TODO
- https://github.com/OSGeo/gdal-docs
- ~~whitebox-tools: https://github.com/jblindsay/whitebox-tools/~~
- geographiclib: https://geographiclib.sourceforge.io/html/utilities.html
- OSSIM(a powerful suite of geospatial libraries and applications used to process imagery, maps, terrain, and vector data.): https://trac.osgeo.org/ossim/wiki/OSSIMCommandLine
- Sentinel Toolbox: https://sentinel.esa.int/web/sentinel/toolboxes
- rsgislib: https://www.rsgislib.org/commandlineutilities.html
- proj4: https://proj4.org/apps/index.html#apps
- PDAL(Point Data Abstraction Library): https://pdal.io/
- ...



## settings
settings.py
- CONCURRENT_REQUESTS
- DOWNLOAD_DELAY



地球科学辞典
http://www.gsdkj.net:81/dict.aspx

如果需要[下载图片](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/media-pipeline.html)，可能出现下列问题：
```
from PIL import Image
  File "D:\ProgramData\Anaconda3\lib\site-packages\PIL\Image.py", line 60, in <module>
    from . import _imaging as core
ImportError: DLL load failed: 找不到指定的模块。
```
>https://github.com/python-pillow/Pillow/issues/2945

LOG_LEVEL = 'WARNING'