不同 gdal utilities 的文档结构存在一定的区别，因此无法完全一次性准确地抓取，
需要在抓取之后根据文档内容进行再次编辑补充。
例如，
- gdalinfo 需要单独处理
- gdaldem 需要单独处理 https://www.gdal.org/gdaldem.html
gdaldem 有多种模式，相当于多个命令，如 gdaldem hillshade，gdaldem slope 等，每种模式参数略有差异

`scrapy crawl gdal_spider -o gdal.json`
**使用新版的文档**
https://github.com/OSGeo/gdal-docs

- gdaldem 有多种模式，相当于多个命令，如 gdaldem hillshade，gdaldem slope 等，每种模式参数略有差异

需要对照原文进行一定的修改，修改之后的位于edited_tools.json

---
问题
gdal_contour
```
       {
        "flag": "-amax",
        "dataType": "String",
        "isOptional": true,
        "available_values": null,
        "name": "name", # 多个参数名称都为name
        "explanation": "Provides a name for the attribute in which to put the maximum elevation of\ncontour polygon. If not provided no maximim elevation attribute is attached.\nIgnored in default line contouring mode. \n \n New in version 2.4.0. \n \n"
      }
      
       {
        "flag": "-snodata",
        "dataType": "String", # Float
        "isOptional": true,
        "name": "value",
        "explanation": "Input pixel value to treat as \u201cnodata\u201d. \n"
      },
      
      #    "example": " -a elev dem.tif contour.shp -i 10.0"
```
-srcnodata 不是 输入文件
gdal_calc.py 参数没有抽出来
gdalbuildvrt 多个参数（如resolution） isOptional 为 false，应为 true
gdal_pansharpen 与 gdal_edit 混在一起