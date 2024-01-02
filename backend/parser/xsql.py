from .ply import lex, yacc
from .interpreter import expr
from .interpreter import stmt
from . import lexRules
from .lexRules import tokens
import re
from parser.interpreter import exceptions

def getPosition(p, token:int):
    '''Returns a tuple containing the line and index of a token'''
    return (p.lineno(token), p.lexpos(token))

lexer = lex.lex(reflags=re.IGNORECASE, module=lexRules)

precedence = (
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
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

def p_block(p):
    '''
    block   : BEGIN stmts END
    '''
    p[0] = stmt.Block(p[2])

def p_return(p):
    '''
    stmt    : RETURN expr
    '''
    p[0] = stmt.Return(p[2])

def p_usar_F(p):
   '''
   stmt    : USAR IDENTIFIER
   '''
   p[0] = stmt.Usar(p[2])

def p_create_base(p):
    '''
    stmt    : CREATE DATA BASE IDENTIFIER
    '''
    p[0] = stmt.CreateBase(p[4])



def p_create_table(p):
    '''
    stmt     : CREATE TABLE IDENTIFIER '(' table_structure ')'
    '''
    p[0]= stmt.CreateTable(p[3], p[5])

def p_truncate_table(p):
    '''
    stmt     : TRUNCATE TABLE IDENTIFIER 
    '''
    p[0] = stmt.Truncate(p[3], getPosition(p, 1))
    
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

def p_column_declaration(p):
    '''
    column_declaration   : IDENTIFIER type nullity key_type foreign_key
    '''
    columnData = {
        'name': p[1],
        'attrib': {
            'type': p[2][0],
            'null': 'no' if p[4] == 'primary' else p[3],
            'key': p[4]
        }
    }
    if p[2][1]:
        columnData['attrib'].update({'length': str(p[2][1])})
    if p[5]:
        columnData['attrib'].update({'reference':f'{p[5][0]}.{p[5][1]}'})
    p[0] = columnData

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

def p_foreign_key(p):
    '''
    foreign_key : REFERENCE IDENTIFIER '(' IDENTIFIER ')'
                | empty
    '''
    if len(p) != 2:
        p[0] = (p[2], p[4])

def p_alter_add(p):
   '''
   stmt : ALTER TABLE IDENTIFIER ADD COLUMN column_declaration
   '''
   p[0] = stmt.AlterADD(p[3], p[6], getPosition(p, 1))

def p_alter_drop(p):
   '''
   stmt : ALTER TABLE IDENTIFIER DROP COLUMN IDENTIFIER 
   '''
   p[0] = stmt.AlterDROP(p[3], p[6], getPosition(p, 1))

def p_drop_table(p):
    '''
    stmt    : DROP TABLE IDENTIFIER
    '''
    p[0] = stmt.DropTable(p[3], getPosition(p, 1))

def p_insert(p):
    '''
    stmt : INSERT INTO IDENTIFIER '(' identifiers ')' VALUES '(' exprs ')'   
    '''
    position = getPosition(p, 1)
    p[0] = stmt.Insert(p[3], p[5], p[9], position)

def p_Delete(p):
    '''
    stmt : DELETE FROM IDENTIFIER where
    '''
    p[0] = stmt.Delete(p[3],p[4],None) 


def p_Update(p):
    '''
    stmt :  UPDATE IDENTIFIER ListNewAssignment where
    '''
    p[0]=stmt.Update(p[2],p[3],p[4])

def p_List_NewAssignment(p):
    '''
    ListNewAssignment   : ListNewAssignment ',' SET IDENTIFIER '=' expr
                        | SET IDENTIFIER '=' expr

    '''
    if len(p) == 6:
        p[0] = p[1]
        p[0].append((p[4], p[6]))
    else:
        p[0] = []
        p[0].append((p[2], p[4]))

def p_identifiers(p):
    '''
    identifiers : identifiers ',' IDENTIFIER
                | IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_exprs(p):
    '''
    exprs   : exprs ',' expr
            | expr
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])
        
    
def p_stmt_declare(p):
    '''
    stmt    : DECLARE '@' IDENTIFIER AS type
            | DECLARE '@' IDENTIFIER type
    '''
    if len(p) == 6:
        p[0] = stmt.Declare('@'+p[3], p[5][0], p[5][1])
    else:
        p[0] = stmt.Declare('@'+p[3], p[4][0], p[4][1])

def p_stmt_assignment(p):
    '''
    stmt    : SET '@' IDENTIFIER '=' expr
    '''
    position = getPosition(p, 3)
    p[0] = stmt.Set('@'+p[3], p[5], position)

def p_stmt_select_from(p):
    '''
    stmt    : SELECT '*' FROM identifiers where
            | SELECT selection_list FROM identifiers where
    '''
    position = getPosition(p, 1)
    p[0] = stmt.SelectFrom(p[4], p[2], p[5], position)

def p_stmt_select(p):
    '''
    stmt    : SELECT selection_list
    '''
    p[0] = stmt.Select(p[2])

def p_selection_list(p):
    '''
    selection_list  : selection_list ',' return_expr alias
                    | return_expr alias
    '''
    if len(p) == 5:
        p[0] = p[1]
        p[0].append((p[3], p[4]))
    else:
        p[0] = []
        p[0].append((p[1], p[2]))

def p_selection_list_case(p):
    '''
    selection_list  : selection_list ',' expr_case
                    | expr_case
    '''
    if len(p) == 2:
        p[0] = [(p[1], None)]
    else:
        p[0] = p[1]
        p[0].append((p[3], None))

def p_return_expr(p):
    '''
    return_expr : expr
                | contar
                | sumar
    '''
    p[0] = p[1]

def p_contar(p):
    '''
    contar  : CONTAR '(' '*' ')'
            | CONTAR '(' symbol ')'
    '''
    p[0] = expr.Contar(p[3], getPosition(p, 1))

def p_sumar(p):
    '''
    sumar   : SUMAR '(' symbol ')'
    '''
    p[0] = expr.Sumar(p[3], getPosition(p, 1))

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

def p_expr_case(p):
    '''
    expr_case   : CASE expr_cases ELSE THEN expr END case_alias
    '''
    p[0] = expr.Case(p[2], p[5], p[7])

def p_expr_cases(p):
    '''
    expr_cases  : expr_cases WHEN expr THEN expr
                | WHEN expr THEN expr
    '''
    if len(p) == 5:
        p[0] = [(p[2], p[4])]
    else:
        p[0] = p[1]
        p[0].append((p[3], p[5]))

def p_case_alias(p):
    '''
    case_alias  : IDENTIFIER
                | STRING_LITERAL
    '''
    p[0] = p[1]

def p_where(p):
    '''
    where   : WHERE condition
            | empty
    '''
    if len(p) == 3:
        p[0] = p[2]

def p_condition_logical(p):
    '''
    condition   : condition LOGICAL_AND condition
                | condition LOGICAL_OR condition
    '''
    position = getPosition(p, 2)
    p[0] = expr.Binary(p[1], p[2], p[3], position)

def p_condition_relational(p):
    '''
    condition   : symbol '<' condition_expr
                | symbol '>' condition_expr
                | symbol LESS_EQUALS condition_expr
                | symbol GREATER_EQUALS condition_expr
                | symbol '=' condition_expr
                | symbol NOT_EQUALS condition_expr
    '''
    position = getPosition(p, 2)
    p[0] = expr.Binary(p[1], p[2], p[3], position)

def p_condition_arithmetic(p):
    '''
    condition_expr  : condition_expr '+' condition_expr
                    | condition_expr '-' condition_expr
                    | condition_expr '/' condition_expr
                    | condition_expr '*' condition_expr
    '''
    position = getPosition(p, 2)
    p[0] = expr.Binary(p[1], p[2], p[3], position)

def p_condition_unary(p):
    '''
    condition_expr  : '!' condition_expr
                    | '-' condition_expr %prec UMINUS
    '''
    position = getPosition(p, 1)
    p[0] = expr.Unary(p[1], p[2], position)

def p_condition_group(p):
    '''
    condition_expr  : '(' condition_expr ')'
    '''
    p[0] = p[2]

def p_condition_base(p):
    '''
    condition_expr  : literal
                    | native
                    | symbol
                    | varCall
    '''
    p[0] = p[1]

def p_ternary_between(p):
    '''
    expr    : expr BETWEEN expr AND expr
    condition   : symbol BETWEEN condition_expr AND condition_expr
    '''
    position = getPosition(p, 2)
    p[0] = expr.Between(p[1], p[3], p[5], position)

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
            | expr LOGICAL_AND expr
            | expr LOGICAL_OR expr
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

def p_expr_base(p):
    '''
    expr    : literal
            | native
            | symbol
            | varCall
    '''
    p[0] = p[1]

def p_literal(p):
    '''
    literal : INT_LITERAL
            | DECIMAL_LITERAL
            | STRING_LITERAL
    '''
    position = getPosition(p, 1)
    p[0] = expr.Literal(p[1], position)

def p_symbol(p):
    '''
    symbol  : symbol '.' IDENTIFIER
            | IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = expr.Symbol(p[1], getPosition(p, 1))
    else:
        p[0] = p[1]
        p[0].key += f'.{p[3]}'

def p_expr_symbol(p):
    '''
    varCall : '@' IDENTIFIER
    '''
    position = getPosition(p, 2)
    p[0] = expr.Symbol('@'+p[2], position)

def p_if_func(p):
    '''
    native  : IF '(' expr ',' expr ',' expr ')'
    '''
    p[0] = expr.If(p[3], p[5], p[7])

def p_concatenar(p):
    '''
    native    :   CONCATENAR '(' exprs ')' 
    '''
    position = getPosition(p, 1)
    p[0] = expr.Concatenar(p[3], position)

def p_substraer(p):
    '''
    native    :   SUBSTRAER '(' exprs ')' 
    '''
    position = getPosition(p, 1)
    p[0] = expr.Substaer(p[3], position)


def p_hoy(p):
    '''
    native    :   HOY '(' ')' 
    '''
    p[0] = expr.Hoy()

def p_type(p):
    '''
    type    : DECIMAL
            | INT
            | DATE
            | DATETIME
    '''
    p[0] = (p[1], None)

def p_type_strings(p):
    '''
    type    : NCHAR '(' INT_LITERAL ')'
            | NVARCHAR '(' INT_LITERAL ')'
    '''
    max = 4000
    if p[1] == 'nvarchar':
        max = 2000000
    if p[3] > max:       
        raise ValueError(f"Error: El valor de nchar debe estar entre 1 y {max}")
    p[0] = (p[1], p[3])

def p_empty(p):
    '''
    empty   :
    '''
    pass

def p_ciclo_While(p):
    '''
    stmt : WHILE expr block
    '''
    p[0] = stmt.Ciclo_while(p[2],p[3])

def p_ssl_If(p):
    '''
    stmt : IF expr block else
    '''
    p[0] = stmt.Ssl_IF(p[2],p[3],p[4])

def p_Fin_If(p):
    '''
    else    : ELSE block
            | empty
    '''
    if len(p) != 2:
        p[0] = p[2]

def p_ssl_Case(p):
    '''
    stmt    : CASE stmt_cases ELSE THEN stmt ';' END
    '''
    p[0] =stmt.Ssl_Case(p[2], p[5])

def p_stmt_cases(p):
    '''
    stmt_cases  : stmt_cases WHEN expr THEN stmt ';'
                | WHEN expr THEN stmt ';'
    '''
    if len(p) == 6:
        p[0] = [(p[2], p[4])]
    else:
        p[0] = p[1]
        p[0].append((p[3], p[5]))

def p_options(p):
    '''
    options   : expr
              | stmt
    '''
    p[0]=p[1]

def p_finCase(p):
    '''
    finCase : IDENTIFIER FROM IDENTIFIER
            | empty
    '''
    p[0]= []
    p[0].append((p[1],p[3]))

# -- Procedimientos
def p_create_procedure(p):
    '''
    stmt    : CREATE PROCEDURE IDENTIFIER '(' parameters ')' AS BEGIN stmts END 
    '''
    p[0] = stmt.Create_procedure(p[3],p[5],p[9])
    
def p_parameters(p):
    '''
    parameters : parameters ',' '@' IDENTIFIER type
                         | '@' IDENTIFIER type
    '''
    if len(p) == 6:
        p[0] = p[1]
        p[0].append(['@'+p[4], p[5]])
    else:
        p[0] = []
        p[0].append(['@'+p[2], p[3]])
        
# -- Llamada procedimientos
def p_exec_procedure(p):
    '''
    stmt    : EXECT IDENTIFIER call_params
    '''

def p_call_params(p):
    '''
    call_params     : call
                    | declare_params
    '''
    
def p_call(p):
    '''
    call    : call ',' expr
            | expr  
    '''
    
def p_declare_params(p):
    '''
    declare_params  : declare_params ',' '@' IDENTIFIER '=' expr
                    | '@' IDENTIFIER '=' expr
    '''
# -- Functions
def p_create_function(p):
    '''
    stmt    : CREATE FUNCTION IDENTIFIER '(' parameters ')' RETURN type AS BEGIN block_stmts END
    '''
    p[0] = stmt.Create_function(p[3],p[5],p[8],p[11])
    
def p_block_stmts(p):
    '''
    block_stmts  : block_stmts stmts
                 | stmts
                 | RETURN expr
    '''    
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = []
        p[0].append(p[1])
    
def p_extend_stmt(p):
    '''
    extend_stmt  : IF, ELSE, DECLARE, SET, INSERT, RETURN, CASE
    '''    
    p[0] = p[1]
    
def p_call_function(p):
    '''
    expr   : IDENTIFIER '(' expr ')'
    '''

def p_error(p):
    if not p:
        raise exceptions.ParsingError(f'Formato de entrada incorrecto', 0)
    error = {
        'type':'sintactico',
        'error':p.value,
        'line':p.lineno,
        'col':p.lexpos
    }
    parser.errors.append(error)
    parser.errok()

parser = yacc.yacc()
