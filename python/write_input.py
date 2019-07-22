# -*- coding: utf-8 -*-

import psycopg2
import re
import os
import codecs
import subprocess

class qgep_swmm:
    
    def __init__(self, title, service, inpfile, inptemplate, outfile):
        self.title = title
        self.service = service
        self.input_file = inpfile
        self.options_template_file = inptemplate
        self.output_file = outfile

    def getSwmmTable(self, tableName):
        
        # Connects to service and get data and attributes from tableName
        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        try:
            cur.execute('select * from qgep_swmm.%s' %tableName)
        except:
            print ('Table %s doesnt exists' %tableName)
            return None, None
        data = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]
        
        return data, attributes
    
    
    def swmmTable(self, tableName):
        # From qgis_swmm
        
        # Create commented line which contains the field names
        fields = ""
        data, attributes = self.getSwmmTable(tableName)
        if data != None:
            for i,field in enumerate(attributes):
                # Does not write values stored in columns descriptions, tags and geom
                if field not in ('description', 'tag', 'geom'):
                    fields+=field +"\t"
            
            # Create input paragraph
            tbl =u'['+tableName+']\n'\
                ';;'+fields+'\n'
            for feature in data:
                for i, v in enumerate(feature):
                    # Write description
                    if attributes[i] == 'description' and str(v) != 'None':
                        tbl += ';'
                        tbl += str(v)
                        tbl += '\n'

                for i, v in enumerate(feature):
                    # Does not write values stored in columns descriptions, tags and geom
                    if attributes[i] not in ('description', 'tag', 'geom'):
                        if str(v) != 'None':
#                            m = re.search('^(\d\d\d\d)-(\d\d)-(\d\d) (\d\d:\d\d):\d\d',str(v)) # for date and time saved as timestamps
#                
#                            if m:
#                                tbl += '/'.join(m.group(2,3,1))+'\t'+m.group(4)+'\t'
#                            else:
                            tbl += str(v)+'\t'
                        else: 
                            tbl += '\t'
                tbl += '\n'
            tbl += '\n'
            return tbl;
        else:
            return '\n'
    
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
                optionText = options_template[indexStart:indexStop]+'\n\n'
            else:
                indexStop = indexStart+1+indexStop  
                optionText = options_template[indexStart:indexStop]
            return optionText
                
        
    def write_input(self):
    
        # From qgis swmm
        print (self.input_file)
        filename = self.input_file
        f = codecs.open(filename, 'w',encoding='utf-8')
        
        #Title / Notes
        #--------------
        f.write('[TITLE]\n')
        f.write(self.title+'\n\n')
        
        # Options
        #--------
        f.write(self.copy_parameters_from_template('OPTIONS'))
        f.write(self.copy_parameters_from_template('REPORT'))
        f.write(self.copy_parameters_from_template('FILES'))
        f.write(self.copy_parameters_from_template('EVENTS'))
        
        # Climatology
        #------------
        f.write(self.copy_parameters_from_template('HYDROGRAPHS'))
        f.write(self.copy_parameters_from_template('EVAPORATION'))
        f.write(self.copy_parameters_from_template('TEMPERATURE'))
       
        # Hydrology
        #----------
        f.write(self.swmmTable('RAINGAGES'))
        f.write(self.swmmTable('SUBCATCHMENTS'))
        f.write(self.swmmTable('SUBAREAS'))
        f.write(self.swmmTable('AQUIFERS'))
        f.write(self.swmmTable('INFILTRATION'))
        f.write(self.swmmTable('POLYGONS'))
        
        
        f.write(self.copy_parameters_from_template('INFLOWS'))
        f.write(self.copy_parameters_from_template('GROUNDWATER'))
        f.write(self.copy_parameters_from_template('SNOWPACKS'))
        f.write(self.copy_parameters_from_template('HYDROGAPHS'))
        f.write(self.copy_parameters_from_template('LID_CONTROLS'))
        f.write(self.copy_parameters_from_template('LID_USAGE'))
        
        # Hydraulics: nodes
        #------------------
        f.write(self.swmmTable('JUNCTIONS'))
        # Create default junction to avoid errors
        f.write('default_qgep_node\t0\t0\n\n')
        f.write(self.swmmTable('OUTFALLS'))
        f.write(self.swmmTable('STORAGE'))
        f.write(self.swmmTable('COORDINATES'))
        
        f.write(self.copy_parameters_from_template('DIVIDERS'))
        
        # Hydraulics: links
        #------------------
        f.write(self.swmmTable('CONDUITS'))
        f.write(self.swmmTable('PUMPS'))
        f.write(self.copy_parameters_from_template('ORIFICES'))
        f.write(self.copy_parameters_from_template('WEIRS'))
        f.write(self.copy_parameters_from_template('OUTLETS'))
        f.write(self.swmmTable('XSECTIONS'))
        f.write(self.swmmTable('LOSSES'))
        f.write(self.swmmTable('VERTICES'))
        
        f.write(self.copy_parameters_from_template('TRANSECTS'))
        f.write(self.copy_parameters_from_template('CONTROLS'))
        
        # Quality
        #--------
        f.write(self.swmmTable('LANDUSES'))
        f.write(self.swmmTable('COVERAGES'))
        
        f.write(self.copy_parameters_from_template('POLLUTANTS'))
        f.write(self.copy_parameters_from_template('BUILDUP'))
        f.write(self.copy_parameters_from_template('WASHOFF'))
        f.write(self.copy_parameters_from_template('TREATMENT'))
        f.write(self.copy_parameters_from_template('DWF'))
        f.write(self.copy_parameters_from_template('RDII'))
        f.write(self.copy_parameters_from_template('LOADINGS'))
        
        # Curves
        #-------
        f.write(self.copy_parameters_from_template('CURVES'))
        
        # Time series
        #------------
        f.write(self.copy_parameters_from_template('TIMESERIES'))
        
        # Time patterns
        #--------------
        f.write(self.copy_parameters_from_template('PATTERNS'))
        
        # Map labels
        #-----------
        f.write(self.copy_parameters_from_template('LABELS'))
        
        f.write(self.swmmTable('TAGS'))

        f.close()
        del f
        
        return
    
    def extract_result_lines(table_title):
        o = codecs.open(self.output_file,'r',encoding='utf-8')
        line = o.readline()
        noLine = 0
        lines=[]
        titleFound=False
        endTableFound = False
        while line:
            line = line.rstrip()
            # Search for the table title
            if line.find(table_title) != -1:
                titleFound = True
                lineAfterTitle = 0
            
            if titleFound and lineAfterTitle > 7 and line == '':
                endTableFound = True
            
            if titleFound and endTableFound == False and lineAfterTitle > 7:
                lines.append(line.split())
                
                
            if titleFound:       
                lineAfterTitle += 1
                
            noLine+=1
            line = o.readline()
        
        return lines
    
    def extract_node_depth_summary():
        
        data = extract_result_lines('Node Depth Summary')
        result = {}
        for d in data:
            curRes = {}
            curRes['id'] = d[0]
            curRes['type'] = d[1]
            curRes['average_depth'] = d[2]
            curRes['maximum_depth'] = d[3]
            curRes['maximum_HGL'] = d[4]
            curRes['time_max_day'] = d[5]
            curRes['time_max_time'] = d[6]
            curRes['reported_max_depth'] = d[7]
            result[d[0]] = curRes
        return result
    
    def extract_link_flow_summary():
        
        data = extract_result_lines('Link Flow Summary')
        result = {}
        for d in data:
            
            curRes = {}
            curRes['id'] = d[0]
            curRes['type'] = d[1]
            curRes['maximum_flow'] = d[2]
            curRes['time_max_day'] = d[3]
            curRes['time_max_time'] = d[4]
            if d[1] == 'CONDUIT':
                curRes['maximum_velocity'] = d[5]
                curRes['max_over_full_flow'] = d[6]
                curRes['max_over_full_depth'] = d[7]
            elif d[1] == 'PUMP':
                curRes['max_over_full_flow'] = d[5]
                
            result[d[0]] = curRes
        return result
    
    def extract_cross_section_summary():
        
        data = extract_result_lines('Cross Section Summary')
        result = {}
        for d in data:
            
            curRes = {}
            curRes['id'] = d[0]
            curRes['shape'] = d[1]
            curRes['full_depth'] = d[2]
            curRes['full_area'] = d[3]
            curRes['hyd_rad'] = d[4]
            curRes['max_width'] = d[5]
            curRes['no_of_barrels'] = d[6]
            curRes['full_flow'] = d[7]
              
            result[d[0]] = curRes
        return result
    
    def save_node_depth_summary():
        con = None
        obj_id = None
        sql = """
        """
        try:
            con = psycopg2.connect(service=self.service)
            cur = con.cursor()
            cur.executemany(sql, (value1,value2))
            obj_id = cur.fetchone()[0]
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
        return obj_id
    
    def save_link_flow_summary():
        return
    
    def save_cross_section_summary():
        return
            
        

PATH2SCHEMA = 'S:/2_INTERNE_SION/0_COLLABORATEURS/PRODUIT_Timothee/02_work/qgep_swmm/scripts/install_swmm_views.bat'
TITLE = 'title simulation'
PGSERVICE = 'pg_qgep_demo_data'
INPFILE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\input\\qgep_swmm.inp'
INPTEMPLATE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\simulation_parameters\\default_qgep_swmm_parameters.inp'
OUTFILE = ''

subprocess.call([PATH2SCHEMA])   
qs = qgep_swmm(TITLE, PGSERVICE, INPFILE, INPTEMPLATE, OUTFILE)
qs.write_input()
print ('done')