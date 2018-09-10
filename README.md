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
