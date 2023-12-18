import xml.etree.ElementTree as ET
from parser.interpreter.database import dml
path = 'databases/'

class Select:
    def __init__(self, exprs:list) -> None:
        self.exprs = exprs

    def interpret(self):
        for expr in self.exprs:
            print(expr[0].interpret(), expr[1], sep=' AS ')

class SelectFrom:
    def __init__(self, selection:list, table:str, condition):
        self.selection = selection
        self.table = table
        self.condition = condition

def writeTreeToFile(tree, file):
    ET.indent(tree)
    tree.write(file, encoding='utf-8', xml_declaration=True)

class createBase:
    def __init__(self, identificator) -> None:
        self.identificator = identificator

    def interpret(self):
        root = ET.Element('database')
        tree = ET.ElementTree(root)
        path = globals()['path'] + self.identificator + '.xml'
        with open(path, 'wb') as file:
            writeTreeToFile(tree, file)

        return ("Base Creada")


class createTable:
    def __init__(self,NameTable,column,base) -> None:
       self.base=base
       self.column=column
       self.NameTable =NameTable
       
    def interpret(self):
        nombreArchivo = globals()['path'] + self.base +'.xml'
        doc = ET.parse(nombreArchivo)
        raiz = doc.getroot()

        Tabla = ET.SubElement(raiz, self.NameTable)
        Columnas =ET.SubElement(Tabla, "columns")
        for column in self.column:
            Columnas.append(ET.Element(column['name'], attrib=column['attrib']))
        Tabla.append(ET.Element('records'))
        writeTreeToFile(doc, nombreArchivo)
        return("Tabla Creda")

class AltertADD:
    def __init__(self,NameTable,column,base) -> None:
       self.base=base
       self.column=column
       self.NameTable =NameTable

    def interpret(self):
        nombreArchivo = globals()['path'] + self.base +'.xml'
        doc = ET.parse(nombreArchivo)
        raiz = doc.getroot()
     
        table = raiz.find(self.NameTable)
        columnas = table.find('columns')
        
        columnas.append(ET.Element(self.column['name'], attrib=self.column['attrib']))
        #print('ggggggggggggggggg')
        writeTreeToFile(doc, nombreArchivo)
       
       
       
       
        #alter table hola add HHHHHHHHH int;
        #nombreArchivo=self.base +'.xml'
        #tree = ET.parse(nombreArchivo)
        #root = tree.getroot()

        #for tabla in root.findall(".//Tabla[@identificator='" + self.NameTable + "']"):
        #    for  columnas in tabla.findall(".//COLUMNAS"):
        #        nueva_columna=ET.Element('COLUMNA',tipo=self.type)
        #        nueva_columna.text = self.column
        #    columnas.append(nueva_columna)


        #tree.write(nombreArchivo)
        #return "Columna Agregada"


class AltertDROP:
    def __init__(self,NameTable,TextColumn,base) -> None:
       self.base=base
       self.TextColumn=TextColumn
       self.NameTable =NameTable
       

    def interpret(self):
        nombreArchivo = globals()['path'] + self.base +'.xml'
        doc = ET.parse(nombreArchivo)
        raiz = doc.getroot()

        table = raiz.find(self.NameTable)
        columnas = table.find('columns')

        columnas.remove(columnas.find(self.TextColumn))
        

        filas = table.find('records')
        fila = filas.findall('record')
        print(fila)
        for element in fila:
            print(element)
            element.remove(element.find(self.TextColumn))
        #fila.remove(fila.findall(self.TextColumn))
        writeTreeToFile(doc, nombreArchivo)

        #alter table tabla_ejemplo drop col_foranea;
        #nombreArchivo=self.base +'.xml'
        #xml_tree = ET.parse(nombreArchivo)
        #root = xml_tree.getroot()

        #for tabla in root.findall(".//Tabla[@identificator='" + self.NameTable + "']"):
        #    for columnas in tabla.findall(".//COLUMNAS"):
        #        for columna in columnas.findall(".//COLUMNA"):
        #            if columna.text == self.TextColumn:
        #                columnas.remove(columna)
        #                xml_tree.write(nombreArchivo)
        #                return "Columna Eliminada"

        #return "Columna no encontrada"

class insertINTO:
    def __init__(self,NameTable,identificatorColumn,ValColumn,base) -> None:
       self.base=base
       self.ValColumn=ValColumn
       self.identificatorColumn=identificatorColumn
       self.NameTable =NameTable
       

    def interpret(self):
        nombreArchivo=self.base +'.xml'
        xml_tree = ET.parse(nombreArchivo)
        root = xml_tree.getroot()

        
        
        for Element in self.identificatorColumn:

            for tabla in root.findall(".//Tabla[@identificator='" + self.NameTable + "']"):
                for columnas in tabla.findall(".//COLUMNAS"):
                    for indice, columna in enumerate(columnas.findall(".//COLUMNA")):
                        
                        if columna.text == Element:

                            if (indice == 0):
                                records = tabla.find(".//RECORDS")
                                if records is None:
                                    records = ET.SubElement(tabla, 'RECORDS')
                                Filas = ET.SubElement(records,'FILAS')                
                            
                            ET.SubElement(Filas,"FILA",corresponde =columna.text).text=str(self.ValColumn[indice])
            xml_tree.write(nombreArchivo)            

        return "Se finalizo"

class Insert:
    def __init__(self, database, table, selection, values, position):
        self.database = database
        self.table = table
        self.selection = selection
        self.values = values
        self.position = position

    def interpret(self):
        dml.Insert(self.database, self.table, self.selection, self.values, self.position)

class usar: 
    def __init__(self,uso) -> None:
        self.uso = uso
    
    def interpret(self):
        return self.uso
