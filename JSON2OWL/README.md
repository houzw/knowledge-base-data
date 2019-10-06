1. crawling 数据抓取（HTML）
2. extractiong 信息抽取（JSON）
3. cleaning 数据清洗（JSON）
4. configuration 转换配置（INI）
5. mapping 知识映射（OWL）


---
- owlready2 在生成实例时，第一个参数若为string，则其为实例名称；若为数字，则生成匿名实例；不给定值时，自动命名
  如 `p = GrassInput(0, prefLabel=locstr(param['parameter'], lang='en'))` 会生成匿名实例（`_:genid[数字序号]`）,在 protege 中该实例无法显示
  如 `p = GrassInput("name", prefLabel=locstr(param['parameter'], lang='en'))` 则实例名称为 name
  如 `p = GrassInput(prefLabel=locstr(param['parameter'], lang='en'))` 则实例名称为 `grassinput[数字序号]` 形式
- (限 windows) 执行 run_all.py，一次生成多个软件的本体
- 加入**shacl**会导致无法推理，报 shacl 的namespace值不是 anyURI类型