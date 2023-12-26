from parser.interpreter.context import Context
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter import expr, operations
from parser.interpreter.database.table import Table
from . import common
import xml.etree.ElementTree as ET

def insert(context:Context, database:str, tableName:str, selection:list, values:list, position:tuple):
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if table == None:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    required = map(lambda e: e.tag, table.findall("columns/*[@null='no']"))
    for column in required:
        if column not in selection:
            raise RuntimeError(f'Columna: {column} es obligatoria', position)
    columns = common.getTableColumns(table)
    records = table.find('records')
    record = ET.Element('record')
    for i in range(len(selection)):
        if selection[i] not in columns.keys():
            raise RuntimeError(f'No se encuentra {selection[i]} en: {tableName}', position)
        columnType = columns[selection[i]]['type']
        typeLength = columns[selection[i]].get('length')
        value = values[i].interpret(context)
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
    textRecords = []
    if condition:
        for record in tableData.records:
            recordContext = Context(context)
            for key, value in record.items():
                recordContext.declare(key, value)
            conditionPassed = condition.interpret(recordContext)
            if not conditionPassed:
                continue
            textRecord = interpretReturnExprs(returnExprs, recordContext, columnList, position)
            textRecords.append(textRecord)
    else:
        for record in tableData.records:
            recordContext = Context(context)
            for key, value in record.items():
                recordContext.declare(key, value)
            textRecord = interpretReturnExprs(returnExprs, recordContext, columnList, position)
            textRecords.append(textRecord)
    return {
        'header': getTableHeader(returnExprs, columnList),
        'records': textRecords
    }


def delete(context:Context, database:str, tableName:str,
    condition:expr.Binary|None, position:tuple):
    tree = common.getDatabaseElementTree(database)
    table = tree.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en: {database}', position)
    columnsData = getTableColumns(table)
    xmlRecords = table.find('records')
 
    if condition:
        for record in xmlRecords.iter('record'):
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
    columnsData = getTableColumns(table)
    xmlRecords = table.find('records')
 
    if condition:
        for record in xmlRecords.iter('record'):
            tableContext = getTableContext(context, columnsData, record)
            conditionPassed = condition.interpret(tableContext)
            for Asignacion in lista:
                    if not conditionPassed:
                        continue
                    print("Clave: ", Asignacion[0] ,"  Valor: ", Asignacion[1])
                    print("Si",record.find(Asignacion[0]))           
                    FilaCambia = record.find(Asignacion[0])
                    if FilaCambia != None:
                        record.find(Asignacion[0]).text = str(Asignacion[1].interpret(context))
                    else:
                        column = ET.Element(Asignacion[0])
                        column.text = str(Asignacion[1].interpret(context))
                        record.append(column)
    common.writeTreeToFile(tree, database)  
    #for Asignacion in lista:
    #    print("Clave: ", Asignacion[0] ,"  Valor: ", Asignacion[1])