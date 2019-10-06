# TauDEM spider
http://hydrology.usu.edu/taudem/taudem5/documentation.html


## postprocessing
cut/remove substring in parameterName (to description)
 - `Output_Parameter_Region_Grid___tif_format_` remove `___tif_format_`
 - `Output_Parameter_Table_Text_File__must_be__txt_or__csv_or__dat_` cut `__must_be__txt_or__csv_or__dat_` to description
 - `Select_Feature_Class_Attribute____FID__is_not_a_valid_attribute_(Optional)` cut `____FID__is_not_a_valid_attribute_` to description

replace ` \r\n      ` to ` `(one space) 
replace ` \r\n ` to ` `(one space) 