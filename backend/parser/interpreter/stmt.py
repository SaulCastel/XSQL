import xml.etree.ElementTree as ET

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

class createBase:
    def __init__(self, identificator) -> None:
        self.identificator = identificator

    def interpret(self):
        nombre = self.identificator +'.xml'
        root = ET.Element(self.identificator)
  
        child1 = ET.SubElement(root, 'child1', )

        tree = ET.ElementTree(root)

        with open(nombre, 'wb') as file:
            tree.write(file, encoding='utf-8', xml_declaration=True)

        return ("Base Creada")


class createTable:
    def __init__(self,NameTable,column,base) -> None:
       self.base=base
       self.column=column
       self.NameTable =NameTable
       
    def interpret(self):
        nombreArchivo=self.base +'.xml'
        doc = ET.parse(nombreArchivo)
        raiz =doc.getroot()
 
        if raiz.find('child1') != None:
            raiz.remove(raiz.find('child1'))



        Tabla = ET.SubElement(raiz,"Tabla",identificator = self.NameTable)
        ValorLlavePrimaria = None
        Columnas =ET.SubElement(Tabla,"COLUMNAS",)
        for Element in self.column:
            if Element[3] == True and ValorLlavePrimaria == None :
                ET.SubElement(Tabla,'PK').text=str(Element[0])
            elif Element[3] == True and ValorLlavePrimaria != None :
                print('ya esxiste una llave primaria')
            else:
                ET.SubElement(Columnas,"COLUMNA",tipo=(Element[1])).text=str(Element[0])
        doc.write(nombreArchivo,xml_declaration=True)

        return("Tabla Creda")
    

class AltertADD:
    def __init__(self,NameTable,column,base, type) -> None:
       self.base=base
       self.column=column
       self.NameTable =NameTable
       self.type = type

    def interpret(self):
        nombreArchivo=self.base +'.xml'
        tree = ET.parse(nombreArchivo)
        root = tree.getroot()

        for tabla in root.findall(".//Tabla[@identificator='" + self.NameTable + "']"):
            for  columnas in tabla.findall(".//COLUMNAS"):
                nueva_columna=ET.Element('COLUMNA',tipo=self.type)
                nueva_columna.text = self.column
            columnas.append(nueva_columna)


        tree.write(nombreArchivo)
        return "Columna Agregada"


class AltertDROP:
    def __init__(self,NameTable,TextColumn,base) -> None:
       self.base=base
       self.TextColumn=TextColumn
       self.NameTable =NameTable
       

    def interpret(self):
        nombreArchivo=self.base +'.xml'
        xml_tree = ET.parse(nombreArchivo)
        root = xml_tree.getroot()

        for tabla in root.findall(".//Tabla[@identificator='" + self.NameTable + "']"):
            for columnas in tabla.findall(".//COLUMNAS"):
                for columna in columnas.findall(".//COLUMNA"):
                    if columna.text == self.TextColumn:
                        columnas.remove(columna)
                        xml_tree.write(nombreArchivo)
                        return "Columna Eliminada"

        return "Columna no encontrada"

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

class usar: 
    def __init__(self,uso) -> None:
        self.uso = uso
    
    def interpret(self):
        return self.uso
