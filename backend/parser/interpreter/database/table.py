from parser.interpreter import operations
from typing_extensions import Self
#from typing import Self
import xml.etree.ElementTree as ET

class Table:
    def __init__(self, name, columnsData:dict[str, dict], records:ET.Element) -> None:
        self.name = name
        self.records:list[dict] = self.loadDataFromEtree(columnsData, records)
        self.columnList:list[str] = list(map(lambda c: f'{name}.{c}', columnsData.keys()))

    def loadDataFromEtree(self, columnsData:dict[str, dict], records:ET.Element):
        castedRecords = []
        for record in records.iter('record'):
            cells = record.findall('./*')
            data = {}
            for cell in cells:
                columnType = columnsData[cell.tag]['type']
                typeLength = columnsData[cell.tag].get('length')
                value = operations.cast(cell.text, columnType)
                name = f'{self.name}.{cell.tag}'
                if typeLength:
                    typeLength = int(typeLength)
                data[name] = operations.wrapInSymbol(name, value, columnType, typeLength)
            missingColumns = list(set(columnsData.keys()) - set(map(lambda c: c.tag, cells)))
            for column in missingColumns:
                columnType = columnsData[column]['type']
                typeLength = columnsData[column].get('length')
                if typeLength:
                    typeLength = int(typeLength)
                name = f'{self.name}.{column}'
                data[name] = operations.wrapInSymbol(name, None, columnType, typeLength)
            castedRecords.append(data)
        return castedRecords
        
    def join(self, table:Self):
        newRecords = []
        for theirRow in table.records:
            for joinedRow in map(lambda ourRow: {**theirRow, **ourRow}, self.records):
                newRecords.append(joinedRow)
        self.records = newRecords
        for column in table.columnList:
            self.columnList.append(column)
