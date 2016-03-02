Pysett - tiny library for parsing the *.xml setting file into python data model

# usage
* xml-structure is super simple
<tab> tag - starts each category
<option> tag - represents single option

# example
xml file :
```
<settings>
   <tab name="general">
       <option name="text size" type="int" default="80"/>
       <option name="font size" type="int" default="20"/>
       <option name="color" type="str" default="black"/>
       <option name="padding" type="int" default="10"/>
   </tab>
</settings>
```

will be converted to :
```
Settings.general.text_size
Settings.general.font_size
Settings.general.color
Settings.general.paddng
```

where Settings is your storage object

# ToDo
* inital commit 
* test files
* fool proof
* gui integration (PyQt)
* export to pip
