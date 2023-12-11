from .ply.lex import lex
from .ply.yacc import yacc
from .interpreter import expr
from . import lexRules
from .lexRules import tokens
import re

def getPosition(p, token:int):
    '''Returns a tuple containing the line and index of a token'''
    return (p.lineno(token), p.lexpos(token))

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
    position = getPosition(p, 2)
    p[0] = expr.Binary(p[1], p[2], p[3], position)

def p_expr_unary(p):
    '''
    expr    : '-' expr %prec UMINUS
            | '!' expr
    '''
    position = getPosition(p, 1)
    p[0] = expr.Unary(p[1], p[2], position)

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

def p_error(p):
  if not p:
    print('Comando invalido')
    return
  print(f'Error de sintaxis en: <{p.value}>')

parser = yacc()
