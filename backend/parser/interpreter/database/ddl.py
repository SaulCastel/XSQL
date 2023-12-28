from . import common
from parser.interpreter.exceptions import RuntimeError
import xml.etree.ElementTree as ET

def createBase(identifier:str):
    root = ET.Element('database')
    tree = ET.ElementTree(root)
    common.writeTreeToFile(tree, identifier)

def createTable(tableName:str, columnList:list[dict], database:str):
    tree = common.getDatabaseElementTree(database)
    raiz = tree.getroot()

    Tabla = ET.SubElement(raiz, tableName)
    Columnas =ET.SubElement(Tabla, "columns")
    for column in columnList:
        Columnas.append(ET.Element(column['name'], attrib=column['attrib']))
    Tabla.append(ET.Element('records'))
    common.writeTreeToFile(tree, database)

def dropTable(database:str, tableName:str, position:tuple):
    tree = common.getDatabaseElementTree(database)
    root = tree.getroot()
    table = root.find(tableName)
    if table == None:
        raise RuntimeError(f'Tabla {tableName} no existe en {database}', position)
    root.remove(table)
    common.writeTreeToFile(tree, database)

def alterAdd(tableName:str, column:dict, database:str, position:tuple):
    tree = common.getDatabaseElementTree(database)
    raiz = tree.getroot()

    table = raiz.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en {database}', position)
    columnas = table.find('columns')

    columnas.append(ET.Element(column['name'], attrib=column['attrib']))
    common.writeTreeToFile(tree, database)

def alterDrop(tableName:str, column:str, database:str, position:tuple):
    tree = common.getDatabaseElementTree(database)
    raiz = tree.getroot()
    table = raiz.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en {database}', position)
    columnas = table.find('columns')
    columnDefinition = columnas.find(column)
    if columnDefinition == None:
        raise RuntimeError(f'No se encuentra {column} en {tableName}', position)
    columnas.remove(columnDefinition)
    filas = table.find('records')
    for element in filas.findall('record'):
        cell = element.find(column)
        if cell != None:
            element.remove(cell)
    common.writeTreeToFile(tree, database)

def truncate(tableName:str, database:str, position:tuple):
    tree = common.getDatabaseElementTree(database)
    raiz = tree.getroot()

    table = raiz.find(tableName)
    if not table:
        raise RuntimeError(f'No se encuentra {tableName} en {database}', position)
    
    filas = table.find("records")
    
    
    filas.clear()
        
    common.writeTreeToFile(tree, database)
    
