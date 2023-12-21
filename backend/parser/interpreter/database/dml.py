from parser.interpreter.context import Context
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter import expr
from parser.interpreter import operations
from . import common
import xml.etree.ElementTree as ET

def getTableColumns(table:ET.Element) -> dict:
    columns = {}
    for element in table.find('columns').findall('./*'):
        columns[element.tag] = element.attrib
    return columns

def insert(context:Context, database:str, tableName:str, selection:list, values:list, position:tuple):
    tree = common.getDatabaseElementTree(database)
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
        columnType = columns[selection[i]]['type']
        value = values[i].interpret(context)
        if not isinstance(value, common.getType(columnType)):
            raise RuntimeError(f'Valor para {selection[i]} debe ser {columnType}, no {type(value).__name__}', position)
        #TODO: raise error on unknown value for foreign key
        column = ET.Element(selection[i])
        if columnType == 'nchar' or columnType == 'nvarchar':
            length = int(columns[selection[i]]['length'])
            if len(value) > length:
                value = value[0:length]
        column.text = str(value)
        record.append(column)
    records.append(record)
    common.writeTreeToFile(tree, database)

def getTableContext(prev:Context, columnsData:dict[str,dict], record: ET.Element) -> Context:
    cells = record.findall('./*')
    context = Context(prev)
    for cell in cells:
        columnType = columnsData[cell.tag]['type']
        columnLength = columnsData[cell.tag].get('length')
        value = operations.cast(cell.text, columnType)
        context.declare(cell.tag, value, common.getType(columnType), columnLength)
    missingColumns = list(set(columnsData.keys()) - set(map(lambda c: c.tag, cells)))
    for column in missingColumns:
        columnType = columnsData[column]['type']
        context.declare(column, None, columnType)
    return context

def interpretReturnExprs(
    returnExprs:list[tuple[expr.Expr, str|None]],
    tableContext:Context,
    columnList,
    position:tuple
) -> list[str]:
    row = []
    if returnExprs == '*':
        for column in columnList:
            row.append(str(tableContext.get(column, position).value))
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

def selectFrom(
    context:Context, database:str, tableName:str,
    returnExprs:list[tuple[expr.Expr, str|None]],
    condition:expr.Binary|None, position:tuple
) -> dict[str, list]:
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    columnsData = getTableColumns(table)
    xmlRecords = table.find('records')
    textRecords = []
    if condition:
        for record in xmlRecords.iter('record'):
            tableContext = getTableContext(context, columnsData, record)
            conditionPassed = condition.interpret(tableContext)
            if not conditionPassed:
                continue
            textRecord = interpretReturnExprs(returnExprs, tableContext, columnsData.keys(), position)
            textRecords.append(textRecord)
    else:
        for record in xmlRecords.iter('record'):
            tableContext = getTableContext(context, columnsData, record)
            textRecord = interpretReturnExprs(returnExprs, tableContext, columnsData.keys(), position)
            textRecords.append(textRecord)
    return {
        'header': getTableHeader(returnExprs, columnsData.keys()),
        'records': textRecords
    }
