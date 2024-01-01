from parser.interpreter.context import Context
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter import expr, operations
from parser.interpreter.database.table import Table
from . import common
import xml.etree.ElementTree as ET

def insert(
    context:Context, database:str, tableName:str,
    selection:list[str], values:list[expr.Expr],
    position:tuple
):
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if table == None:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    columns = common.getTableColumns(table)
    for column in selection:
        if column in columns.keys(): continue
        raise RuntimeError(f'No se encuentra {column} en: {tableName}', position)
    required = map(lambda e: e.tag, table.findall("columns/*[@null='no']"))
    for column in required:
        if column in selection: continue
        raise RuntimeError(f'Columna: {column} es obligatoria', position)
    primaryKey = tuple(map(lambda e: e.tag, table.findall('columns/*[@key="primary"]')))
    rowData = {}
    for i in range(len(selection)):
        rowData[selection[i]] = values[i].interpret(context)
    newUniqueValue = list(map(lambda key: str(rowData[key]), primaryKey))
    records = table.find('records')
    for record in records.iter('record'):
        pKey = list(map(lambda key: record.find(key).text, primaryKey))
        if newUniqueValue != pKey: continue
        raise RuntimeError(f'Valor para llave primaria {primaryKey} repetido', position)
    record = ET.Element('record')
    for i in range(len(selection)):
        columnType = columns[selection[i]]['type']
        typeLength = columns[selection[i]].get('length')
        value = rowData.get(selection[i])
        if typeLength:
            typeLength = int(typeLength)
        wrapedValue = operations.wrapInSymbol(selection[i], value, columnType, typeLength)
        #TODO: raise error on unknown value for foreign key
        column = ET.Element(selection[i])
        column.text = str(wrapedValue)
        record.append(column)
    records.append(record)
    common.writeTreeToFile(tree, database)

def interpretReturnExprs(
    returnExprs:list[tuple[expr.Expr, str|None]],
    recordContext:Context,
    columnList,
    position:tuple
) -> list[str]:
    row = []
    if returnExprs == '*':
        for column in columnList:
            row.append(str(recordContext.get(column, position).value))
    else:
        for e in returnExprs:
            row.append(str(e[0].interpret(recordContext)))
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
    context:Context, database:str, tables:list[str],
    returnExprs:list[tuple[expr.Expr, str|None]],
    condition:expr.Binary|None, position:tuple
) -> dict[str, list]:
    databaseTree = common.getDatabaseElementTree(database)
    tableData = []
    for tableName in tables:
        table = databaseTree.find(tableName)
        if not table:
            raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
        columnsData = common.getTableColumns(table)
        xmlRecords = table.find('records')
        if not xmlRecords: continue
        tableData.append(Table(tableName, columnsData, xmlRecords))
    if len(tables) > 1:
        leftTable:Table = tableData[0]
        for i in range(1, len(tableData)):
            leftTable.join(tableData[i])
        tableData = leftTable
    else:
        tableData = tableData[0]
    columnList = tableData.columnList
    records = []
    if condition:
        for record in tableData.records:
            recordContext = Context(context)
            for key, value in record.items():
                recordContext.declare(key, value)
            conditionPassed = condition.interpret(recordContext)
            if not conditionPassed:
                continue
            records.append(recordContext)
    else:
        for record in tableData.records:
            recordContext = Context(context)
            for key, value in record.items():
                recordContext.declare(key, value)
            records.append(recordContext)
    textRecords = []
    if type(returnExprs[0][0]) == expr.Contar or type(returnExprs[0][0]) == expr.Sumar:
        textRecords.append([str(returnExprs[0][0].interpret(records))])
    else:
        for record in records:
            textRecord = interpretReturnExprs(returnExprs, record, columnList, position)
            textRecords.append(textRecord)
    return {
        'header': getTableHeader(returnExprs, columnList),
        'records': textRecords
    }

def getTableContext(prev:Context, columnsData:dict[str,dict], record: ET.Element) -> Context:
    cells = record.findall('./*')
    context = Context(prev)
    for cell in cells:
        columnType = columnsData[cell.tag]['type']
        columnLength = columnsData[cell.tag].get('length')
        if columnLength: columnLength = int(columnLength)
        value = operations.cast(cell.text, columnType)
        symbol = operations.wrapInSymbol(cell.tag, value, columnType, columnLength)
        context.declare(cell.tag, symbol)
    missingColumns = list(set(columnsData.keys()) - set(map(lambda c: c.tag, cells)))
    for column in missingColumns:
        columnType = columnsData[column]['type']
        symbol = operations.wrapInSymbol(column, None, columnType)
        context.declare(column, symbol)
    return context

def delete(context:Context, database:str, tableName:str,
    condition:expr.Binary|None, position:tuple):
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    columnsData = common.getTableColumns(table)
    xmlRecords = table.find('records')
    if condition:
        for record in xmlRecords.findall('record'):
            tableContext = getTableContext(context, columnsData, record)
            conditionPassed = condition.interpret(tableContext)
            if not conditionPassed:
                continue
            xmlRecords.remove(record)
    else:
        xmlRecords.clear()
    common.writeTreeToFile(tree, database)

def update(context:Context,database:str,tableName:str,condition:expr.Binary|None, lista :list ):
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}')
    columnsData = common.getTableColumns(table)
    xmlRecords = table.find('records')
 
    if condition:
        for record in xmlRecords.findall('record'):
            tableContext = getTableContext(context, columnsData, record)
            conditionPassed = condition.interpret(tableContext)
            for Asignacion in lista:
                    if not conditionPassed:
                        continue
                    FilaCambia = record.find(Asignacion[0])
                    if FilaCambia != None:
                        record.find(Asignacion[0]).text = str(Asignacion[1].interpret(context))
                    else:
                        column = ET.Element(Asignacion[0])
                        column.text = str(Asignacion[1].interpret(context))
                        record.append(column)
    common.writeTreeToFile(tree, database)  
