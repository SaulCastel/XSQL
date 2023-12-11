from .ply.lex import TOKEN
from datetime import datetime, date
from .interpreter import types

reserved = {
    'null': 'NULL'
}

tokens = [
    'LESS_EQUALS', 'GREATER_EQUALS', 'EQUALS', 'NOT_EQUALS', 'AND', 'OR',
    'DECIMAL_LITERAL','INT_LITERAL', 'STRING_LITERAL', 'DATE_LITERAL', 'DATETIME_LITERAL',
    'UMINUS'
] + list(reserved.values())

literals = ['+','-','/','*','<','>','!', '@']

number = r'([0-9]+)'
decimal = f'({number}[.]{number})'
string = r'("[^"]*")'
dateRegex = r'((0[1-9]|[12][0-9]|[3[01]])-(0[1-9]|1[0-2])-(1[7-9]|[2-9]\d)\d\d)'
zeroToSixty = r'(0[0-9]|[1-5][0-9])'
dateTimeRegex = f'({date} ([01][0-9]|2[0-3]):{zeroToSixty}:{zeroToSixty})'

t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_AND = r'&&'
t_OR = r'\|\|'

@TOKEN(dateTimeRegex)
def t_DATETIME_LITERAL(t):
    date_time = t.value.split()
    date = date_time[0].split('-')
    t.value = datetime.fromisoformat(f'{date[2]}-{date[1]}-{date[0]} {date_time[1]}')
    return t

@TOKEN(dateRegex)
def t_DATE_LITERAL(t):
    date_split = t.value.split('-')
    t.value = date.fromisoformat(f'{date_split[2]}-{date_split[1]}-{date_split[0]}')
    return t

@TOKEN(decimal)
def t_DECIMAL_LITERAL(t):
    t.value = types.DECIMAL(t.value)
    return t

@TOKEN(number)
def t_INT_LITERAL(t):
    t.value = types.INT(t.value)
    return t

@TOKEN(string)
def t_STRING_LITERAL(t):
    t.value = types.NCHAR(t.value.strip('"'), 100)
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

def t_error(t):
  print(f'Error lexico en: <{t.value}>')
  t.lexer.skip(1)
