from parser.interpreter.context import Context
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter import expr
from parser.interpreter import operations
import xml.etree.ElementTree as ET
import config

def writeTreeToFile(tree, file):
    ET.indent(tree)
    tree.write(file, encoding='utf-8', xml_declaration=True)

def getTableColumns(table:ET.Element) -> dict:
    columns = {}
    for element in table.find('columns').findall('./*'):
        columns[element.tag] = element.attrib
    return columns

def Insert(database:str, tableName:str, selection:list, values:list, position:tuple):
    tree = ET.parse(config.pathToDatabases + f'{database}.xml')
    table = tree.find(tableName)
    if table == None:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    required = map(lambda e: e.tag, table.findall("columns/*[@null='no']"))
    for column in required:
        if column not in selection:
            raise RuntimeError(f'Columna: {column} es obligatoria', position)
    columns = getTableColumns(table)
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

def getTableContext(columnsData:dict, record: ET.Element) -> Context:
    cells = record.findall('./*')
    context = Context()
    for cell in cells:
        columnType = columnsData[cell.tag]['type']
        context.declare(cell.tag, operations.cast(cell.text, columnType))
    missingColumns = list(set(columnsData.keys()) - set(map(lambda c: c.tag, cells)))
    for column in missingColumns:
        context.declare(column, None)
    return context

def interpretReturnExprs(
        returnExprs:list[tuple[expr.Expr, str|None]],
        tableContext:Context,
        columnList:list
) -> list[str]:
    row = []
    if returnExprs == '*':
        for column in columnList:
            row.append(str(tableContext.get(column).value))
    else:
        for e in returnExprs:
            row.append(str(e[0].interpret(tableContext)))
    return row

def getTableHeader(returnExprs:list[tuple[expr.Expr, str|None]], columnList) -> list[str]:
    header = []
    if returnExprs == '*':
        for column in columnList:
            header.append(column)
    else:
        for item in returnExprs:
            if item[1]:
                header.append(item[1])
            else:
                header.append(str(item[0]))
    return header

def Select(
    position:tuple, database:str, tableName:str,
    returnExprs:list[tuple[expr.Expr, str|None]],
    condition:expr.Binary|None=None
) -> dict[str, list]:
    tree = ET.parse(config.pathToDatabases + f'{database}.xml')
    table = tree.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    columnsData = getTableColumns(table)
    xmlRecords = table.find('records')
    textRecords = []
    if condition:
        for record in xmlRecords.iter('record'):
            tableContext = getTableContext(columnsData, record)
            result = condition.interpret(tableContext)
            if result:
                textRecords.append(interpretReturnExprs(returnExprs, tableContext, columnsData.keys()))
    else:
        for record in xmlRecords.iter('record'):
            tableContext = getTableContext(columnsData, record)
            textRecords.append(interpretReturnExprs(returnExprs, tableContext, columnsData.keys()))
    return {
        'header': getTableHeader(returnExprs, columnsData.keys()),
        'records': textRecords
    }
