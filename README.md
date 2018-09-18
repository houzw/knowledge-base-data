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


## 转换为owl本体
- 去除csv或json中不合法的Unicode字符
- 设计本体模型，包括类的层次结构的组织，属性和关系的设计等
- JSON2OWL下编写转换方法并执行。如
  - csdms2owl.py
  - taudem2owl.py
- 检查修正