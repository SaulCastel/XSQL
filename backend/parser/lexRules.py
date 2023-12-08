from .ply.lex import TOKEN

reserved = {
    'null': 'NULL'
}

tokens = [
    'LESS_EQUALS', 'GREATER_EQUALS', 'EQUALS', 'NOT_EQUALS', 'AND', 'OR',
    'DECIMAL_LITERAL','INT_LITERAL', 'STRING_LITERAL', 'DATE_LITERAL', 'DATETIME_LITERAL',
    'UMINUS'
] + list(reserved.values())

literals = ['+','-','/','*','<','>','!']

number = r'([0-9]+)'
decimal = f'({number}[.]{number})'
string = r'("[^"]*")'
date = r'((0[1-9]|[1-2][0-9]|[3[01]])-(0[1-9]|1[0-2])-(1[7-9]|[2-9]\d)\d\d)'
zeroToSixty = r'(0[0-9]|[1-5][0-9])'
dateTime = f'({date} (0[0-9]|[10-19]2[0-3]):{zeroToSixty}:{zeroToSixty})'

t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_AND = r'&&'
t_OR = r'\|\|'

@TOKEN(dateTime)
def t_DATETIME_LITERAL(t):
    return t

@TOKEN(date)
def t_DATE_LITERAL(t):
    return t

@TOKEN(decimal)
def t_DECIMAL_LITERAL(t):
    return t

@TOKEN(number)
def t_INT_LITERAL(t):
    return t

@TOKEN(string)
def t_STRING_LITERAL(t):
    return t.strip('"')

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

def t_error(t):
  print(f'Error lexico en: <{t.value}>')
  t.lexer.skip(1)
