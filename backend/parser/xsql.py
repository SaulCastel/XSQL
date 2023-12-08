from .ply.lex import lex
from .ply.yacc import yacc
from .interpreter import expr
from . import lexRules
from .lexRules import tokens
import re

lexer = lex(reflags=re.IGNORECASE, module=lexRules)

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

def p_start(p):
    '''
    script  : exprs
    '''
    p[0] = p[1]

def p_exprs_rec(p):
    '''
    exprs   : exprs expr
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_exprs_element(p):
    '''
    exprs   : expr
    '''
    p[0] = []
    p[0].append(p[1])

def p_expr_binary(p):
    '''
    expr    : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
    '''
    p[0] = expr.Binary(p[1], p[2], p[3])

def p_expr_unary(p):
    '''
    expr    : '-' expr %prec UMINUS
            | '!' expr
    '''
    p[0] = expr.Unary(p[1], p[2])

def p_expr_int_literal(p):
    '''
    expr    : INT_LITERAL
    '''
    p[0] = expr.Literal(p[1], 'int')

def p_expr_decimal_literal(p):
    '''
    expr    : DECIMAL_LITERAL
    '''
    p[0] = expr.Literal(p[1], 'decimal')

def p_error(p):
  if not p:
    print('Comando invalido')
    return
  print(f'Error de sintaxis en: <{p.value}>')

parser = yacc()
