from parser.interpreter import expr
def createBase(identifier:str,contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="CREATE DATABASE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{identifier}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n'
    return  dot 

def createTable(tableName:str, columnList:list[dict],contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="CREATE TABLE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n'
    cuentaElemento =0
    for column in columnList:
        if "reference" in column["attrib"]:
            dot += f'"Elemento{contador}_{cuentaElemento}" [label="{column["name"]}  {column["attrib"]["type"]} {column["attrib"]["key"]} Reference ( {column["attrib"]["reference"]} ) "]\n'
        else:
            dot += f'"Elemento{contador}_{cuentaElemento}" [label="{column["name"]}  {column["attrib"]["type"]} {column["attrib"]["key"]}"]\n'
        
        dot += f'"identificador{contador}" -- "Elemento{contador}_{cuentaElemento}"\n'
      
        cuentaElemento+=1
        
    return dot


def truncate(tableName:str, contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="TRUNCATE TABLE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n'
    return  dot 

def alterAdd(tableName:str, column:dict, contador: int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="ALTER TABLE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n' 
    dot += f'"add{contador}" [label="ADD COLUMN"]\n'
    dot += f'"{contador}" -- "add{contador}" \n'
    dot += f'"Elemento{contador}" [label="{column["name"]}  {column["attrib"]["type"]} {column["attrib"]["key"]}"]\n'
    dot += f'"add{contador}"--Elemento{contador} \n'
    return dot

def alterDrop(tableName:str, column:str,contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="ALTER TABLE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n' 
    dot += f'"add{contador}" [label="DROP COLUMN"]\n'
    dot += f'"{contador}" -- "add{contador}" \n'
    dot += f'"text{contador}" [label="{column}"]\n'
    dot += f'"add{contador}"--text{contador} \n'
    return dot

def dropTable(tableName:str,contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="DROP TABLE"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n' 
    return dot

def insert(tableName:str,selection:list[str], values:list[expr.Expr],contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="INSERT INTO"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n' 
    dot += f'"columnas{contador}" [label="COLUMNAS"]\n'
    dot += f'"identificador{contador}" -- "columnas{contador}" \n'
    dot += f'"values{contador}" [label="VALUES"]\n'
    dot += f'"identificador{contador}" -- "values{contador}" \n'
    cuentaElemento =0
    for Element in selection:
        dot += f'"Col{contador}_{cuentaElemento}" [label="{Element}"]\n'
        dot += f'"columnas{contador}" -- "Col{contador}_{cuentaElemento}"\n'
        cuentaElemento+=1

    cuentaElemento =0
    for Element in values:
        dot += Element.GenerarAST()
        dot += f'"values{contador}" -- "{Element.contador}"\n'
        cuentaElemento+=1
    return dot 

def delete(tableName:str,condition:expr.Binary|None, contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="DELETE FROM"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    dot += f'"identificador{contador}" [label="{tableName}"]\n'
    dot += f'"{contador}" -- "identificador{contador}"\n'
    if condition != None:
        dot += f'"where{contador}" [label="WHERE"]\n'
        dot += f'"{contador}" -- "where{contador}"\n'
        dot += condition.GenerarAST()
        dot += f'"where{contador}" -- "{condition.contador}"\n'
    return dot 

def selectFrom(
    tables:list[str],returnExprs:list[tuple[expr.Expr, str|None]],
    condition:expr.Binary|None,contador:int):
    dot = f'"stmt{contador}" [label="stmt"]\n'
    dot += f'"{contador}" [label="SELECT"]\n'
    dot += f'"stmt{contador}" -- "{contador}" \n'
    if returnExprs !=None:
        for Expr in returnExprs:
            dot += Expr[0].GenerarAST()
            dot += f'"{contador}" -- "{Expr[0].contador}" \n'
    dot += f'"from{contador}" [label="FROM"]\n'
    dot += f'"{contador}" -- "from{contador}" \n'
    Element=0
    for table in tables:
        dot += f'"tables{contador}_{Element}" [label="{table}"]\n'
        dot += f'"from{contador}" -- "tables{contador}_{Element}" \n'
        Element +=1
    if condition != None:
        dot += f'"where{contador}" [label="WHERE"]\n'
        dot += f'"from{contador}" -- "where{contador}"\n'
        dot += condition.GenerarAST()
        dot += f'"where{contador}" -- "{condition.contador}"\n'
    return dot