import psycopg2
import re
import os
import codecs

def getSwmmTable(service, tableName):
    
    # Connects to service and get data and attributes from tableName
    con = psycopg2.connect(service=service)
    cur = con.cursor()
    cur.execute('select * from %s' %tableName)
    data = cur.fetchall()
    attributes = [desc[0] for desc in cur.description]
    
    return data, attributes


def swmmTable(service, tableName):
    # From qgis_swmm
    
    # Create commented line which contains the field names
    fields = ""
    data, attributes = getSwmmTable(service, tableName)
    for i,field in enumerate(attributes): 
        fields+=field +"\t"
    
    # Create input paragraph
    tbl =u'['+tableName+']\n'\
        ';'+fields+'\n'
    for feature in data:
        for i, v in enumerate(feature):
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

def write_input(service, title):
    # From qgis swmm
    
    folder = 'C://temp//'
    filename = os.path.join(folder, 'swmm.inp')
    f = codecs.open(filename,'w',encoding='utf-8')
    f.write('[TITLE]\n')
    f.write(title,'\n\n')
    f.write(swmmTable(service, 'qgep_swmm.junctions_copy'))
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