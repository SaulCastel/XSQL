from .ply import lex, yacc
from .interpreter import expr
from .interpreter import stmt
from . import lexRules
from .lexRules import tokens
import re

BaseEnUso = '  '

def getPosition(p, token:int):
    '''Returns a tuple containing the line and index of a token'''
    return (p.lineno(token), p.lexpos(token))

lexer = lex.lex(reflags=re.IGNORECASE, module=lexRules)

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', '!'),
    ('left', 'EQUALS', 'NOT_EQUALS', '<', '>', 'LESS_EQUALS', 'GREATER_EQUALS'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

def p_start(p):
    '''
    script  : stmts
    '''
    p[0] = p[1]

def p_stmts(p):
    '''
    stmts   : stmts stmt ';'
            | stmt ';'
    '''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = []
        p[0].append(p[1])

def p_usar_F(p):
   '''
   stmt    : USAR IDENTIFIER
   '''
   p[0] = stmt.usar(p[2])
   global BaseEnUso
   BaseEnUso = p[2]

def p_create_base(p):
    '''
    stmt    : CREATE DATA BASE IDENTIFIER
    '''
    global BaseEnUso
    BaseEnUso = p[4]

    p[0] = stmt.createBase(p[4])


def p_create_table(p):
    '''
    stmt     : CREATE TABLE IDENTIFIER '(' List_Table ')'

    '''
    p[0]= stmt.createTable(p[3],p[5],BaseEnUso)


def p_list_table1(p):
   '''
   List_Table       : List_Table IDENTIFIER type ','
                    | List_Table IDENTIFIER type
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],False,False])


def p_list_table2(p):
   '''
   List_Table        : IDENTIFIER type ','
                     | IDENTIFIER type 
   '''
   p[0] = []
   p[0].append([p[1],p[2],False,False]) 


def p_list_table3(p):
   '''
   List_Table       : List_Table IDENTIFIER type NOT NULL ','
                    | List_Table IDENTIFIER type NOT NULL
                    | List_Table IDENTIFIER type NULL ','
                    | List_Table IDENTIFIER type NULL
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],True,False])

def p_list_table4(p):
   '''
   List_Table        : IDENTIFIER type NOT NULL ','
                     | IDENTIFIER type NOT NULL
                     | IDENTIFIER type NULL ','
                     | IDENTIFIER type NULL
   '''
   p[0] = []
   p[0].append([p[1],p[2],True,False]) 

def p_list_table_primaria1(p):
   '''
   List_Table        : List_Table IDENTIFIER type NOT NULL PRIMARY KEY ','
                     | List_Table IDENTIFIER type NOT NULL PRIMARY KEY
                     | List_Table IDENTIFIER type NULL PRIMARY KEY ','
                     | List_Table IDENTIFIER type NULL PRIMARY KEY
                     | List_Table IDENTIFIER type PRIMARY KEY ','
                     | List_Table IDENTIFIER type PRIMARY KEY
   '''
   p[0] = p[1]
   p[0].append([p[2],p[3],True,True]) 


def p_list_table_primaria2(p):
   '''
   List_Table        : IDENTIFIER type NOT NULL PRIMARY KEY ','
                     | IDENTIFIER type NOT NULL PRIMARY KEY
                     | IDENTIFIER type NULL PRIMARY KEY ','
                     | IDENTIFIER type NULL PRIMARY KEY
                     | IDENTIFIER type PRIMARY KEY ','
                     | IDENTIFIER type PRIMARY KEY
   '''
   p[0] = []
   p[0].append([p[1],p[2],True,True]) 


def p_inst_Altert(p):
   '''
   stmt : Altert_Table_ADD
                | Altert_Table_DROP
   '''
   p[0] = p[1]
   

def p_alter_add(p):
   '''
   Altert_Table_ADD  : ALTER TABLE IDENTIFIER ADD IDENTIFIER type
   '''
   p[0] = stmt.AltertADD(p[3],p[5],BaseEnUso,p[6])

def p_alter_drop(p):
   '''
   Altert_Table_DROP  : ALTER TABLE IDENTIFIER DROP IDENTIFIER 
   '''
   p[0] = stmt.AltertDROP(p[3],p[5],BaseEnUso)

def p_insert_fila(p):
   '''
   stmt : INSERT INTO IDENTIFIER '(' List_identificadores ')' VALUES '(' List_identificadores ')'   
   '''
   p[0] = stmt.insertINTO(p[3],p[5],p[9],BaseEnUso)


def p_lista_identificadores1(p):
   '''
   List_identificadores       : List_identificadores IDENTIFIER 
                              | List_identificadores IDENTIFIER ',' 
   '''
   p[0] = p[1]
   p[0].append(p[2])
    

def p_lista_identificadores2(p):
   '''
   List_identificadores       : IDENTIFIER ','
                              | IDENTIFIER
   '''
   p[0] = []
   p[0].append(p[1]) 

def p_stmt_variable(p):
    '''
    stmt    : DECLARE '@' IDENTIFIER AS type
    '''
    position = getPosition(p, 2)
    p[0] = stmt.Declare(p[3], p[5], position)

def p_stmt_select_from(p):
    '''
    stmt    : SELECT '*' FROM IDENTIFIER where
            | SELECT selection_list FROM IDENTIFIER where
    '''
    p[0] = stmt.SelectFrom(p[2], p[4], p[5])

def p_stmt_select(p):
    '''
    stmt    : SELECT selection_list
    '''
    p[0] = stmt.Select(p[2])

def p_selection_list(p):
    '''
    selection_list  : selection_list ',' expr alias
                    | expr alias
    '''
    if len(p) == 5:
        p[0] = p[1]
        p[0].append((p[3], p[4]))
    else:
        p[0] = []
        p[0].append((p[1], p[2]))

def p_alias(p):
    '''
    alias   : AS IDENTIFIER
            | AS STRING_LITERAL
            | empty
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_where(p):
    '''
    where   : WHERE condition
            | empty
    '''
    pass

def p_condition_chain(p):
    '''
    condition   : condition AND condition
                | condition OR condition
    '''
    pass

def p_condition_base(p):
    '''
    condition   : IDENTIFIER '<' expr
                | IDENTIFIER '>' expr
                | IDENTIFIER LESS_EQUALS expr
                | IDENTIFIER GREATER_EQUALS expr
                | IDENTIFIER EQUALS expr
                | IDENTIFIER NOT_EQUALS expr
    '''
    pass

def p_expr_binary(p):
    '''
    expr    : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '>' expr
            | expr '<' expr
            | expr LESS_EQUALS expr
            | expr GREATER_EQUALS expr
            | expr EQUALS expr
            | expr NOT_EQUALS expr
            | expr AND expr
            | expr OR expr
    '''
    position = getPosition(p, 2)
    p[0] = expr.Binary(p[1], p[2], p[3], position)

def p_expr_unary(p):
    '''
    expr    : '-' expr %prec UMINUS
            | '!' expr
    '''
    position = getPosition(p, 1)
    p[0] = expr.Unary(p[1], p[2], position)

def p_expr_group(p):
    '''
    expr    : '(' expr ')'
    '''
    p[0] = p[2]

def p_expr_literal(p):
    '''
    expr    : INT_LITERAL
            | DECIMAL_LITERAL
            | DATE_LITERAL
            | DATETIME_LITERAL
            | STRING_LITERAL
    '''
    position = getPosition(p, 1)
    p[0] = expr.Literal(p[1], position)

def p_expr_variable(p):
    '''
    expr    : '@' IDENTIFIER
    '''
    position = getPosition(p, 2)
    p[0] = expr.Variable(p[2], position)

def p_type(p):
    '''
    type    : DECIMAL
            | INT
            | DATE
            | DATETIME
    '''
    p[0] = p[1]

def p_type_strings(p):
    '''
    type    : NCHAR '(' INT_LITERAL ')'
            | NVARCHAR '(' INT_LITERAL ')'
    '''
    pass

def p_empty(p):
    '''
    empty   :
    '''
    pass

def p_error(p):
  if not p:
    print('Comando invalido')
    return
  print(f'Error de sintaxis en: <{p.value}>')

parser = yacc.yacc()
