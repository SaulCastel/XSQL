from .ply.lex import lex
from .ply.yacc import yacc
#from .interpreter import expr

from . import lexRules
from .lexRules import tokens
import re


from .interpreter import instruction


lexer = lex(reflags=re.IGNORECASE, module=lexRules)

BaseEnUso = '  '
def p_start(p):
    '''
    script  : instructions
    '''
    p[0] = p[1]

def p_instructions_rec(p):
    '''
    instructions   : instructions instruction
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_instructions_element(p):
    '''
    instructions   : instruction
    '''
    p[0] = []
    p[0].append(p[1])

def p_usar_F(p):
   '''
   instruction    : USAR IDENTIFICATOR_F PyC
   '''
   p[0] = instruction.usar(p[2])
   global BaseEnUso
   BaseEnUso = p[2]

def p_create_base(p):
    '''
    instruction    : CREATE DATA BASE IDENTIFICATOR_F PyC
    '''
    global BaseEnUso
    BaseEnUso = p[4]

    p[0] = instruction.createBase(p[4])


def p_create_table(p):
    '''
    instruction     : CREATE TABLE IDENTIFICATOR_F PARENTESIS_A List_Table PARENTESIS_B PyC

    '''
    p[0]= instruction.createTable(p[3],p[5],BaseEnUso)


def p_list_table1(p):
   '''
   List_Table       : List_Table IDENTIFICATOR_F Type_Primitive COMMA
                    | List_Table IDENTIFICATOR_F Type_Primitive
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],False,False])


def p_list_table2(p):
   '''
   List_Table        : IDENTIFICATOR_F Type_Primitive COMMA
                     | IDENTIFICATOR_F Type_Primitive 
   '''
   p[0] = []
   p[0].append([p[1],p[2],False,False]) 


def p_list_table3(p):
   '''
   List_Table       : List_Table IDENTIFICATOR_F Type_Primitive NOT NULL COMMA
                    | List_Table IDENTIFICATOR_F Type_Primitive NOT NULL
                    | List_Table IDENTIFICATOR_F Type_Primitive NULL COMMA
                    | List_Table IDENTIFICATOR_F Type_Primitive NULL
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],True,False])

def p_list_table4(p):
   '''
   List_Table        : IDENTIFICATOR_F Type_Primitive NOT NULL COMMA
                     | IDENTIFICATOR_F Type_Primitive NOT NULL
                     | IDENTIFICATOR_F Type_Primitive NULL COMMA
                     | IDENTIFICATOR_F Type_Primitive NULL
   '''
   p[0] = []
   p[0].append([p[1],p[2],True,False]) 

def p_list_table_primaria1(p):
   '''
   List_Table        : List_Table IDENTIFICATOR_F Type_Primitive NOT NULL PRIMARY KEY COMMA
                     | List_Table IDENTIFICATOR_F Type_Primitive NOT NULL PRIMARY KEY
                     | List_Table IDENTIFICATOR_F Type_Primitive NULL PRIMARY KEY COMMA
                     | List_Table IDENTIFICATOR_F Type_Primitive NULL PRIMARY KEY
                     | List_Table IDENTIFICATOR_F Type_Primitive PRIMARY KEY COMMA
                     | List_Table IDENTIFICATOR_F Type_Primitive PRIMARY KEY
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],True,True]) 


def p_list_table_primaria2(p):
   '''
   List_Table        : IDENTIFICATOR_F Type_Primitive NOT NULL PRIMARY KEY COMMA
                     | IDENTIFICATOR_F Type_Primitive NOT NULL PRIMARY KEY
                     | IDENTIFICATOR_F Type_Primitive NULL PRIMARY KEY COMMA
                     | IDENTIFICATOR_F Type_Primitive NULL PRIMARY KEY
                     | IDENTIFICATOR_F Type_Primitive PRIMARY KEY COMMA
                     | IDENTIFICATOR_F Type_Primitive PRIMARY KEY
   '''
   p[0] = []
   p[0].append([p[1],p[2],True,True]) 


def p_inst_Altert(p):
   '''
   instruction : Altert_Table_ADD
                | Altert_Table_DROP
   '''
   p[0] = p[1]
   

def p_alter_add(p):
   '''
   Altert_Table_ADD  : ALTERT TABLE IDENTIFICATOR_F ADD IDENTIFICATOR_F Type_Primitive
   '''
   p[0] = instruction.AltertADD(p[3],p[5],BaseEnUso,p[6])

def p_alter_drop(p):
   '''
   Altert_Table_DROP  : ALTERT TABLE IDENTIFICATOR_F DROP IDENTIFICATOR_F 
   '''
   p[0] = instruction.AltertDROP(p[3],p[5],BaseEnUso)

def p_insert_fila(p):
   '''
   instruction : INSERT INTO IDENTIFICATOR_F PARENTESIS_A List_identificadores PARENTESIS_B VALUES PARENTESIS_A List_identificadores PARENTESIS_B PyC  
   '''
   p[0] = instruction.insertINTO(p[3],p[5],p[9],BaseEnUso)


def p_lista_identificadores1(p):
   '''
   List_identificadores       : List_identificadores IDENTIFICATOR_F 
                              | List_identificadores IDENTIFICATOR_F COMMA 
   '''
   p[0] = p[1]
   p[0].append(p[2])
    

def p_lista_identificadores2(p):
   '''
   List_identificadores       : IDENTIFICATOR_F COMMA
                              | IDENTIFICATOR_F
   '''
   p[0] = []
   p[0].append(p[1]) 
   
def p_type_primitive_INT(p):
  '''
  Type_Primitive : INT
  ''' 
  p[0]='INT'

def p_type_primitive_BIT(p):
  '''
  Type_Primitive : BIT
  '''   
  p[0]='BIT'

def p_type_primitive_DECIMAL(p):
  '''
  Type_Primitive : DECIMAL
  ''' 
  p[0]='DECIMAL'
   
def p_type_primitive_DATE(p):
  '''
  Type_Primitive : DATE
  ''' 
  p[0]='DATE'

def p_type_primitive_DATETIME(p):
      '''
      Type_Primitive : DATETIME
      ''' 
      p[0]='DATETIME'
def p_type_primitive_NCHAR(p):
      '''
      Type_Primitive : NCHAR 
      '''     
      p[0]='NCHAR'
def p_type_primitive_NVARCHAR(p):
   '''
   Type_Primitive :  NVARCHAR 
   '''
   p[0]='NVARCHAR'

def p_error(p):
  if not p:
    print('Comando invalido')
    return
  print(f'Error de sintaxis en: <{p.value}>')

parser = yacc()