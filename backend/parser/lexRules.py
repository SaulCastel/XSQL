from .ply.lex import TOKEN

reserved = {
    'where': 'WHERE',
    'select': 'SELECT',
    'from': 'FROM',
    'declare': 'DECLARE',
    'create': 'CREATE',
    'data':'DATA',
    'base':'BASE',
    'table':'TABLE',
    'procedure':'PROCEDURE',
    'function':'FUNCTION',
    'return': 'RETURN',
    'as':'AS',
    'begin':'BEGIN',
    'end':'END',
    'alter':'ALTER',
    'add':'ADD',
    'drop':'DROP',
    'int':'INT',
    'decimal':'DECIMAL',
    'date':'DATE',
    'datetime':'DATETIME',
    'nchar':'NCHAR',
    'nvarchar':'NVARCHAR',
    'usar' : 'USAR',
    'insert': 'INSERT',
    'into': 'INTO',
    'values':'VALUES',
    'primary':'PRIMARY',
    'reference':'REFERENCE',
    'key':'KEY',
    'not':'NOT',
    'null':'NULL',
    'concatenar':'CONCATENAR',
    'substraer':'SUBSTRAER',
    'hoy':'HOY',
    'contar':'CONTAR',
    'set':'SET',
    'truncate':'TRUNCATE',
    'delete':'DELETE',
    'update':'UPDATE',
    'while':'WHILE',
    'begin':'BEGIN',
    'end':'END',
    'if':'IF',
    'case':'CASE',
    'when':'WHEN',
    'then':'THEN',
    'else':'ELSE',
    'sumar':'SUMAR',
    'between':'BETWEEN',
    'and':'AND',
}

tokens = [
    'LESS_EQUALS', 'GREATER_EQUALS', 'EQUALS', 'NOT_EQUALS', 'LOGICAL_AND',
    'LOGICAL_OR', 'DECIMAL_LITERAL', 'INT_LITERAL', 'STRING_LITERAL', 'IDENTIFIER',
] + list(reserved.values())

literals = ['+', '-', '/', '*', '<', '>', '!', '@', '(', ')', ';', ',', '=', '.']

number = r'([0-9]+)'
decimal = f'({number}[.]{number})'
doubleQuoteString = r'("[^"]*")'
singleQuoteString = r"('[^']*')"
string = f'({doubleQuoteString}|{singleQuoteString})'
identifier = r'[a-z_][a-z0-9_]*'

t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LOGICAL_AND = r'&&'
t_LOGICAL_OR = r'\|\|'

@TOKEN(decimal)
def t_DECIMAL_LITERAL(t):
    t.value = float(t.value)
    return t

@TOKEN(number)
def t_INT_LITERAL(t):
    t.value = int(t.value)
    return t

@TOKEN(string)
def t_STRING_LITERAL(t):
    t.value = t.value.strip('"\'')
    return t

@TOKEN(identifier)
def t_IDENTIFIER(t):
    t.value = t.value.lower()
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

def t_error(t):
  print(f'Error lexico en: <{t.value}>')
  t.lexer.skip(1)
