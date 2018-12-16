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
- 在 SWATArticle 目录下执行命令：
  `scrapy crawl swat_article -o articles.csv`
- 在 CSDMS 目录下执行
  `scrapy crawl csdms -o csdms.json`
- 在 TauDEM 目录下执行
  `scrapy crawl taudem -o taudem.json`
- 在 SAGA 目录下执行
    `scrapy crawl saga -o saga.json`
- Grass 下
    `scrapy crawl grass -o grass.json`

## 转换为owl本体
- 去除csv或json中不合法的Unicode字符
- 设计本体模型，包括类的层次结构的组织，属性和关系的设计等
- JSON2OWL下编写转换方法并执行。如
  - csdms2owl.py
  - taudem2owl.py
- 检查修正

## 性能设置
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
