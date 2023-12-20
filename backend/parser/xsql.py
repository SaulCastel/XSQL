from .ply import lex, yacc
from .interpreter import expr
from .interpreter import stmt
from . import lexRules
from .lexRules import tokens
import re

from .interpreter import Nativas 
from .interpreter import cadenas
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
    stmt     : CREATE TABLE IDENTIFIER '(' table_structure ')'

    '''
    p[0]= stmt.createTable(p[3],p[5],BaseEnUso)

def p_table_structure(p):
    '''
    table_structure : table_structure ',' column_declaration
                    | column_declaration
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_column_foreign(p):
    '''
    column_declaration  : IDENTIFIER type nullity REFERENCE IDENTIFIER '(' IDENTIFIER ')'
    '''
    p[0] = {
        'name': p[1],
        'attrib': {
            'type': p[2],
            'null': 'no',
            'key': 'foreign',
            'reference': f'{p[5]}.{p[7]}'
        }
    }

def p_column_declaration(p):
    '''
    column_declaration   : IDENTIFIER type nullity key_type
    '''
    p[0] = {
        'name': p[1],
        'attrib': {
            'type': p[2],
            'null': 'no' if p[4] == 'primary' else p[3],
            'key': p[4]
        }
    }

def p_column_nullity(p):
    '''
    nullity             : NOT NULL
                        | NULL
                        | empty
    '''
    if len(p) == 2:
        p[0] = 'yes'
    else:
        p[0] = 'no'

def p_column_key_type(p):
    '''
    key_type            : PRIMARY KEY
                        | empty
    '''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = ''

def p_alter_add(p):
   '''
   stmt : ALTER TABLE IDENTIFIER ADD column_declaration
   '''
   p[0] = stmt.AltertADD(p[3],p[5],BaseEnUso)

def p_alter_drop(p):
   '''
   stmt : ALTER TABLE IDENTIFIER DROP IDENTIFIER 
   '''
   p[0] = stmt.AltertDROP(p[3],p[5],BaseEnUso)

def p_insert_fila(p):
   '''
   stmt : INSERT INTO IDENTIFIER '(' List_identificadores ')' VALUES '(' List_identificadores ')'   
   '''
   p[0] = stmt.insertINTO(p[3],p[5],p[9],BaseEnUso)


def p_lista_identificadores(p):
    '''
    List_identificadores    : List_identificadores ',' IDENTIFIER
                            | IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])
    
def p_stmt_variable(p):
    '''
    stmt    : DECLARE '@' IDENTIFIER AS type
            | DECLARE '@' IDENTIFIER type
    '''
    position = getPosition(p, 2)
    if len(p) == 6:
        p[0] = stmt.Declare(p[3], p[5], position)
    else:
        p[0] = stmt.Declare(p[3], p[4], position)

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
    condition   : symbol '<' expr
                | symbol '>' expr
                | symbol LESS_EQUALS expr
                | symbol GREATER_EQUALS expr
                | symbol '=' expr
                | symbol NOT_EQUALS expr
    '''
    pass

def p_symbol(p):
    '''
    symbol  : symbol '.' IDENTIFIER
            | IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = ([p[1]], getPosition(p, 1))
    else:
        position = p[1][1]
        p[0] = (p[1].append(p[3]), position)

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

def p_expr_symbol(p):
    '''
    expr    : '@' IDENTIFIER
            | symbol
    '''
    if len(p) == 2:
        p[0] = expr.Symbol(p[1][0], p[1][1])
    else:
        position = getPosition(p, 2)
        p[0] = expr.Symbol([p[2]], position)

def p_expr_concatena(p):
    '''
    expr    :   CONCATENAR '(' expr ',' expr ')' 
    '''
    p[0] = Nativas.Concatenar(p[3],p[5])

def p_expr_substrae(p):
    '''
    expr    :   SUBSTRAER '(' expr ',' expr ',' expr ')' 
    '''
    p[0] = Nativas.Substaer(p[3],p[5],p[7])


def p_expr_hoy(p):
    '''
    expr    :   HOY '(' ')' 
    '''
    p[0] = Nativas.hoy()

def p_expr_contar(p):
    '''
    expr     : CONTAR '(' '*' ')' FROM IDENTIFIER where   
    '''
    p[0] = Nativas.contar(p[6],p[8],BaseEnUso)

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
    #p[0] = p[1]
    if str(p[1])=="nchar":
        if int(p[3])>1 and int(p[3])<4000:       
            p[0]="nchar ("+ str(p[3]) + ")"
        else:
            raise ValueError("Error: El valor de nchar debe estar entre 1 y 4000")
    else:
        if int(p[3])<2000000:
            p[0]="nvarchar ("+int(p[3])+")"
        else:
            raise ValueError("Error: El valor maxiomo de nvarchar es de 2,000,000")
   # p[0] = cadenas.TiposDeCadenas(p[1],p[3])

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
