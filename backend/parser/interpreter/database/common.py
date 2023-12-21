import config
from typing import Any
import xml.etree.ElementTree as ET
from datetime import date, datetime

def writeTreeToFile(tree:ET.ElementTree, database:str):
    ET.indent(tree)
    path = config.pathToDatabases+f'{database}.xml'
    tree.write(path, encoding='utf-8', xml_declaration=True)

def getDatabaseElementTree(database:str):
    path = config.pathToDatabases+f'{database}.xml'
    return ET.parse(path)

def getType(t:str) -> Any:
    if t == 'int':
        return int
    elif t == 'decimal':
        return float
    elif t == 'date':
        return date
    elif t == 'datetime':
        return datetime
    else:
        return str
