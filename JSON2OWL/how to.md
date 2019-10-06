## how to write a scirpt to map process knowledge in json format to GeoProBase ontologies

>Based on Owlready2: https://pythonhosted.org/Owlready2/

- define process module (i.e., a geoprocessing software) uri, e.g.,` 'http://www.egc.org/ont/process/arcgis'`, and owlready2 ontology

    ```python
    from owlready2 import *
    import json
    from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
    
    module_uri = 'http://www.egc.org/ont/process/arcgis'
    onto = get_ontology(module_uri)
    ```

- load common ontologies (gb for gis-base, cyber for gis-software)

    ```python
    onto, shacl, skos, dcterms, props = OWLUtils.load_common(onto)
    onto, gb, task, data, cyber = OWLUtils.load_common_for_process_tool(onto)
    onto = OWLUtils.load_geo_vocabl(onto)

    print('ontologies imported')
    ```

- add ontology meatadata

    ```python
    onto.metadata.creator.append('houzhiwei')
    onto.metadata.title.append('ArcGIS Tools')
    import datetime
    onto.metadata.created.append(datetime.datetime.today())
    onto.metadata.versionInfo.append('10.1')
    ```

- define subclasses for this module

    ```python
    with onto:
    	class ArcGISTool(gb.GeoprocessingTool):
    		pass
    	class ArcGISInput(gb.InputData):
    		pass
    	class ArcGISOutput(gb.OutputData):
    		pass
    	class ArcGISOption(gb.Option):
    		pass
    ```

- read json data

    ```python
    module_path = os.path.dirname(__file__)
    with open(module_path + '/arcgis.json', 'r') as f:
    	jdata = json.load(f)  # list
    ```

- **mapping json data to ontology**

    - general information

        - preprocess tool name string
        - create tool instance
        - extract keywords and linked to domain ontologies (csdms-standard-names, gcmd-keywords, hydrology and dta ontology)
        - add general properties according to properties in **json** data and their **corresponding properties** (might be the same name or not) pre-defined in **gis-base** ontology

        ```python
        for d in jdata:
        	"""mapping json data to ontology properties"""
        	# preprocess tool name string
            name_str = ''
            # or just use methods defined in JSON2OWL.OwlConvert.Preprocessor
        	name = re.match("[0-9a-zA-Z\-/* ]+ (?=\([\w' ]+\))", d['name'])
        	if name:
        		name_str = name.group().strip().lower().replace(' ', '_').replace('/', '_')
        	else:
        		continue
            # create tool instance
            # tool classes may be dynamically created according the tool category, e.g., '3D Analyst'
            # `OWLUtils.create_onto_class(onto, tool_cls, ArcGISTool)`
        	tool = ArcGISTool(name_str, prefLabel=locstr(name_str, lang='en'))
            
        	# extract keywords from tool name and summary or description
            # if there are keywords data in json, use them to link to domain ontologies. e.g., in grass
            # OWLUtils.link_to_domain_concept(onto, tool, d['keywords'].append(name.split('.')[1])) # e.g., r.spread

        	keywords = OWLUtils.to_keywords(d['summary'])
	        keywords.append(name_str.replace('_', ' '))

        	# search and link keywords to domain ontologies
            OWLUtils.link_to_domain_concept(onto,tool,keywords)
            
        	# add general properties
        	tool.isToolOfSoftware.append(cyber.ArcGIS_Desktop)
        	tool.hasIdentifier = name_str.replace('_', ' ')
        	# tool.hasManualPageURL.append(d['manual_url'])
        	# tool.description.append(locstr(d['description'], lang='en'))
        	tool.description.append(locstr(d['summary'], lang='en'))
        	# tool.definition.append(d['definition'])
        	tool.hasUsage.append(OWLUtils.join_list(d['usage']))
        	tool.hasSyntax.append(d['syntax'])
        	tool.example.append(handle_example(d['example']))
            # handle task
        	handle_task(d['name'], name_str, d['summary'])
            # handle parameters
        	for parameter in d['parameters']:
        		handle_parameters(parameter)
        
        ```

     - handle task

        ```python
        def handle_task(full_name, task_name, des):
            # read config
        	config = OWLUtils.get_config(module_path + '/config.ini')
            # get task type from full name (tool name)
        	task_type_partten = "\([a-zA-Z0-9*\-' ]+\)"
        	task_types = re.findall(task_type_partten, full_name)
        	if len(task_types) > 1:
        		tool.hasKeywords.append(Preprocessor.remove_parenthesis(task_types[0]))
        		task_type = Preprocessor.remove_parenthesis(re.findall(task_type_partten, full_name)[-1])
        	else:
        		task_type =  Preprocessor.remove_parenthesis(re.findall(task_type_partten, full_name)[0])
        	# get pre-defined task class according to task type from config
            task_cls = config.get('task', task_type)
        	tool.hasKeywords.append(task_type)
        	# create task instance and avoid duplicate
        	if not task[task_name + "_task"]:
        		task_ins = task[task_cls](task_name + "_task", prefLabel=locstr(task_name.replace('_', ' ') + " task", lang='en'))
        		task_ins.isAtomicTask = True
        	else:
        		task_ins = task[task_name + "_task"]
            # general task properties
        	if (task_ins in tool.usedByTask) is False:
        		tool.usedByTask.append(task_ins)
        	if (tool in tool.hasProcessingTool) is False:
        		task_ins.hasProcessingTool.append(tool)
        	task_ins.description.append(locstr(des, lang='en'))
        ```

        `config.ini` (task type = task_cls)

        ```ini
        [task]
        Geostatisical Analyst = Geostatistic
        Spatial Statistics = Geostatistic
        Linear Referencing = LinearReferencing
        3D Analyst = VoxelAnalysis 
        ```

     - handle tool parameters

        ```python
        def handle_parameters(param):
        	if 'isInputFile' in param.keys() and param['isInputFile']:
        		p = ArcGISInput(prefLabel=locstr(param['name'], lang='en'))
        		# p = ArcGISInput(0, prefLabel=locstr(param['name'], lang='en')) # blank node
        		tool.hasInputData.append(p)
        		p.isInputFile = param['isInputFile']
        	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
        		p = ArcGISOutput(prefLabel=locstr(param['name'], lang='en'))
        		tool.hasOutputData.append(p)
        		p.isOutputFile = param['isOutputFile']
        	else:
                # options
        		p = ArcGISOption( prefLabel=locstr(param['name'], lang='en'))
        		tool.hasOption.append(p)
            # general parameter properties
        	p.hasParameterName=param['name']
        	if 'type' in param.keys() and param['type']:
        		p.hasDataTypeStr.append(param['type'])
        	p.description.append(param['desc'])
        	p.isOptional = param['isOptional']
        	datatype = param['type']
        ```

        for grass

        ```python
        def handle_parameters(param):
        	if 'isInputFile' in param.keys() and param['isInputFile']:
        		p = GrassInput(prefLabel=locstr(param['parameter'], lang='en'))
        		# p = GrassInput(0, prefLabel=locstr(param['parameter'], lang='en')) # blank node
        		tool.hasInputData.append(p)
        		p.isInputFile = param['isInputFile']
        	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
        		p = GrassOutput(prefLabel=locstr(param['parameter'], lang='en'))
        		tool.hasOutputData.append(p)
        		p.isOutputFile = param['isOutputFile']
        	else:
        		p = GrassOption(prefLabel=locstr(param['parameter'], lang='en'))
        		tool.hasOption.append(p)
            # general parameter properties
        	p.hasFlag.append(param['flag'])
        	p.hasParameterName = param['parameter']
        	if 'dataType' in param.keys():
        		p.hasDataTypeStr.append(param['dataType'])
        	p.description.append(param['explanation'])
        	if 'defaultValue' in param.keys():
        		if param['defaultValue'] is not None: p.hasDefaultValue = param['defaultValue']
        	p.isOptional = param['optional']
        	if 'alternatives' in param.keys():
        		if param['alternatives']:
                   p.hasAlternatives.append(OWLUtils.join_keywords(param['alternatives']))
        ```

        

- save generated data

    ```python
    # save generated ontology as owl file in rdf xml format
    onto.save(file='arcgis.owl', format="rdfxml")
    # update task ontology
    task.save()
    print('ArcGIS Done!')
    ```

## how to integrate ontologies
   run `Statistic/merge.py`
   
## clear and generate again
sometimes, we may encounter errors or just have modified the ontology structure or spider items or what ever
that we have to generate ontologies again, we must:
- replace(overwrite) the old predefined ontologies with those modified predefined ontologies (optional)
- deleted generated owl files (Strongly recommend)
- deleted `task.owl`, create a new copy of `task_backup.owl` and rename it as `task.owl`. 
  Otherwise, task items won't generate again
- execute modified spider/mapping script again
- the newly crawled json must copied to the folder of each mapping script
   

