# -*- coding: utf-8 -*-

import psycopg2
import re
import os
import codecs

class qgep_swmm:
    
    def __init__(self):
        self.title = 'title simulation'
        self.service = 'pg_qgep_demo_data'
        self.input_file = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\input\\qgep_swmm.inp'
        self.options_template_file = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\simulation_parameters\\example1.inp'
        self.output_file = ''

    def getSwmmTable(self, tableName):
        
        # Connects to service and get data and attributes from tableName
        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        cur.execute('select * from qgep_swmm.%s' %tableName)
        data = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]
        
        return data, attributes
    
    
    def swmmTable(self, tableName):
        # From qgis_swmm
        
        # Create commented line which contains the field names
        fields = ""
        data, attributes = self.getSwmmTable(tableName)
        for i,field in enumerate(attributes):
            # Does not write values stored in columns descriptions, tags and geom
            if field not in ('description', 'tag', 'geom'):
                fields+=field +"\t"
        
        # Create input paragraph
        tbl =u'['+tableName+']\n'\
            ';'+fields+'\n'
        for feature in data:
            for i, v in enumerate(feature):
                # Does not write values stored in columns descriptions, tags and geom
                if attributes[i] not in ('description', 'tag', 'geom'):
                    if str(v) != 'None':
                        m = re.search('^(\d\d\d\d)-(\d\d)-(\d\d) (\d\d:\d\d):\d\d',str(v)) # for date and time saved as timestamps
            
                        if m:
                            tbl += '/'.join(m.group(2,3,1))+'\t'+m.group(4)+'\t'
                        else:
                            tbl += str(v)+'\t'
                    else: 
                        tbl += '\t'
            tbl += '\n'
        tbl += '\n'
        return tbl;
    
    def swmmKeyVal(self, table_name, simul_title):
        
        # Get data from qgis table
    #    uri = self.getParameterValue(table_name)
    #    if not uri: return u''
    #    layer = dataobjects.getObjectFromUri(uri)
    #    fields = []
    #    for i,field in enumerate(layer.dataProvider().fields()): 
    #        fields.append(field.name())
        
        # Create input paragraph
        tbl =u'['+table_name+']\n'
        found = False
        for feature in layer.getFeatures():
            if str(feature[0]) == simul_title:
                for i,v in enumerate(feature):
                    if i and str(v) != 'NULL': tbl += fields[i].upper()+'\t'+str(v)+'\n'
                    elif i : tbl += '\t'
                found = True
                tbl += '\n'
        tbl += '\n'
        if not found:
            raise GeoAlgorithmExecutionException(
                    "No simulation named '"+simul_title+"' in "+table_name)
        return tbl;
    
    def copy_parameters_from_template(self, parameter_name):
        # Read template
        options_template = open(self.options_template_file,'r').read()
        # Find and extract options
        indexStart = options_template.find('[%s]' %parameter_name)
        if indexStart == -1:
            # The balise options is not found
            print ('There is no [%s] in the template file' %parameter_name)
            return ''
        else:
            # Search for the next opening bracket
            indexStop = options_template[indexStart+1:].find('[')
            if indexStop == -1:
                # Copies text until the end of the file
                indexStop = len(options_template)
            else:
                indexStop = indexStart+1+indexStop  
            optionText = options_template[indexStart:indexStop]
            return optionText
                
        
    def write_input(self):
    
        
        
        # From qgis swmm
        print (self.input_file)
        filename = self.input_file
        f = codecs.open(filename, 'w',encoding='utf-8')
        f.write('[TITLE]\n')
        f.write(self.title+'\n\n')
        
        # Copies options from template 
        #-----------------------------
        f.write(self.copy_parameters_from_template('OPTIONS'))
        f.write(self.copy_parameters_from_template('REPORT'))
        f.write(self.copy_parameters_from_template('FILES'))
        f.write(self.copy_parameters_from_template('RAINGAGES'))
        f.write(self.copy_parameters_from_template('HYDROGRAPHS'))
        f.write(self.copy_parameters_from_template('EVAPORATION'))
        f.write(self.copy_parameters_from_template('TEMPERATURE'))
        
        f.write(self.swmmTable('SUBCATCHMENTS'))
#        f.write(self.swmmTable('SUBAREAS'))
#        f.write(self.swmmTable('INFILTRATION'))
        
        
        f.write(self.copy_parameters_from_template('LID_CONTROLS'))
        f.write(self.copy_parameters_from_template('LID_USAGE'))
        f.write(self.copy_parameters_from_template('AQUIFERS'))
        f.write(self.copy_parameters_from_template('GROUNDWATER'))
        f.write(self.copy_parameters_from_template('SNOWPACKS'))
        
#        f.write(self.swmmTable('JUNCTIONS'))
#        f.write(self.swmmTable('OUTFALLS'))
#        f.write(self.swmmTable('DIVIDERS'))
#        f.write(self.swmmTable('STORAGE'))
#        f.write(self.swmmTable('CONDUITS'))
#        f.write(self.swmmTable('PUMPS'))
#        f.write(self.swmmTable('ORIFICES'))
#        f.write(self.swmmTable('WEIRS'))
#        f.write(self.swmmTable('OUTLETS'))
#        f.write(self.swmmTable('XSECTIONS'))
#        f.write(self.swmmTable('LOSSES'))
        
        f.write(self.copy_parameters_from_template('TRANSECTS'))
        f.write(self.copy_parameters_from_template('CONTROLS'))
        f.write(self.copy_parameters_from_template('POLLUTANTS'))
        f.write(self.copy_parameters_from_template('LANDUSES'))
        f.write(self.copy_parameters_from_template('COVERAGES'))
        f.write(self.copy_parameters_from_template('BUILDUP'))
        f.write(self.copy_parameters_from_template('WASHOFF'))
        f.write(self.copy_parameters_from_template('TREATMENT'))
        f.write(self.copy_parameters_from_template('INFLOWS'))
        f.write(self.copy_parameters_from_template('DWF'))
        f.write(self.copy_parameters_from_template('PATTERNS'))
        f.write(self.copy_parameters_from_template('RDII'))
        f.write(self.copy_parameters_from_template('LOADINGS'))
        f.write(self.copy_parameters_from_template('CURVES'))
        f.write(self.copy_parameters_from_template('TIMESERIES'))
        
        
        # currently not used 
        # f.write(self.swmmTable('TAGS'))

        
        
        # f.write(self.swmmTable('qgep_swmm.junctions_copy'))
    #    f.write(self.swmmKeyVal(self.OPTIONS, self.getParameterValue(self.TITLE)))
    #    f.write(self.swmmKeyVal(self.REPORT,self.getParameterValue(self.TITLE)))
    #    f.write(self.swmmTable(self.FILES))
    #    f.write(self.swmmTable(self.RAINGAGES))
    #    f.write(self.swmmTable(self.HYDROGRAPHS))
    #    f.write(self.swmmKeyVal(self.EVAPORATION, self.getParameterValue(self.TITLE)))
    #    f.write(self.swmmTable(self.TEMPERATURE))
    #    f.write(self.swmmTable(self.SUBCATCHMENTS))
    #    f.write(self.swmmTable(self.SUBAREAS))
    #    f.write(self.swmmTable(self.INFILTRATION))
    #    f.write(self.swmmTable(self.LID_CONTROLS))
    #    f.write(self.swmmTable(self.LID_USAGE))
    #    f.write(self.swmmTable(self.AQUIFERS))
    #    f.write(self.swmmTable(self.GROUNDWATER))
    #    f.write(self.swmmTable(self.SNOWPACKS))
    #    f.write(self.swmmTable(self.JUNCTIONS))
    #    f.write(self.swmmTable(self.OUTFALLS))
    #    f.write(self.swmmTable(self.DIVIDERS))
    #    f.write(self.swmmTable(self.STORAGE))
    #    f.write(self.swmmTable(self.CONDUITS))
    #    f.write(self.swmmTable(self.PUMPS))
    #    f.write(self.swmmTable(self.ORIFICES))
    #    f.write(self.swmmTable(self.WEIRS))
    #    f.write(self.swmmTable(self.OUTLETS))
    #    f.write(self.swmmTable(self.XSECTIONS))
    #    f.write(self.swmmTable(self.TRANSECTS))
    #    f.write(self.swmmTable(self.LOSSES))
    #    f.write(self.swmmTable(self.CONTROLS))
    #    f.write(self.swmmTable(self.POLLUTANTS))
    #    f.write(self.swmmTable(self.LANDUSES))
    #    f.write(self.swmmTable(self.COVERAGES))
    #    f.write(self.swmmTable(self.BUILDUP))
    #    f.write(self.swmmTable(self.WASHOFF))
    #    f.write(self.swmmTable(self.TREATMENT))
    #    f.write(self.swmmTable(self.INFLOWS))
    #    f.write(self.swmmTable(self.DWF))
    #    f.write(self.swmmTable(self.PATTERNS))
    #    f.write(self.swmmTable(self.RDII))
    #    f.write(self.swmmTable(self.LOADINGS))
    #    f.write(self.swmmTable(self.CURVES))
    #    f.write(self.swmmTable(self.TIMESERIES))
        f.close()
        
        return
    
qs = qgep_swmm()
qs.write_input()