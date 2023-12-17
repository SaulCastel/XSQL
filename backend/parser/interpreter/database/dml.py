from ..exceptions import RuntimeError
import xml.etree.ElementTree as ET

def writeTreeToFile(tree, file):
    ET.indent(tree)
    tree.write(file, encoding='utf-8', xml_declaration=True)

def Insert(database:str, tableName:str, selection:list, values:list, position:tuple):
    path = f'databases/{database}.xml'
    tree = ET.parse(path)
    table = tree.find(tableName)
    if table == None:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    required = map(lambda e: e.tag, table.findall("columns/*[@null='no']"))
    for column in required:
        if column not in selection:
            raise RuntimeError(f'Columna: {column} es obligatoria', position)
    columns = {}
    for element in table.find('columns').iter():
        columns[element.tag] = element.attrib
    records = table.find('records')
    record = ET.Element('record')
    for i in range(len(selection)):
        if selection[i] not in columns.keys():
            raise RuntimeError(f'No se encuentra {selection[i]} en: {tableName}', position)
        columType = columns[selection[i]]['type']
        value = values[i].interpret()
        valueType = type(value).__name__
        if valueType != columType:
            raise RuntimeError(f'Valor para {selection[i]} debe ser {columType}, no {valueType}', position)
        #TODO: raise error on unknown value for foreign key
        column = ET.Element(selection[i])
        column.text = str(value)
        record.append(column)
    records.append(record)
    writeTreeToFile(tree, path)
