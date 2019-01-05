导入的本体中（skos、software等），应该避免存在间接导入的本体（已经导入的除外，例如skos），否则 owlready 会自动尝试连接网络下载，从而报错
若有，则可以注释掉

在生成本体时， task.owl 会被修改，增加 task 实例及 hasProcessTool 属性