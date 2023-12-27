from typing import Any

from parser.interpreter import symbol
from .exceptions import RuntimeError
from datetime import date, datetime
from parser.interpreter import exceptions

def isDate(left, right) -> bool:
    return isinstance(left, (date, datetime)) or isinstance(right, (date, datetime))

def bothAreNumbers(left, right) -> bool:
    return isinstance(left, (int, float)) and isinstance(right, (int, float))

def isString(left, right) -> bool:
    return isinstance(left, (str)) or isinstance(right, (str))

def sum(left, right, position):
    if isDate(left, right):
        leftType = type(left).__name__
        rightType = type(right).__name__
        raise RuntimeError(f'No se puede sumar/concatenar {leftType} con {rightType}', position)
    elif isString(left, right):
        return str(left) + str(right)
    else:
        return left + right

def sub(left, right, position):
    if not bothAreNumbers(left, right):
        lefttype = type(left).__name__
        righttype = type(right).__name__
        raise RuntimeError(f'no se puede restar {lefttype} con {righttype}', position)
    return left - right

def mult(left, right, position):
    if bothAreNumbers(left, right):
        return left * right
    elif isinstance(left, (str)):
        if isinstance(right, (date, datetime)):
            return left + str(right)
    elif isinstance(left, (date, datetime)):
        if isinstance(right, (str)):
            return str(left) + right
    lefttype = type(left).__name__
    righttype = type(right).__name__
    raise RuntimeError(f'no se puede multiplicar {lefttype} con {righttype}', position)

def div(left, right, position):
    if bothAreNumbers(left, right):
        return left / right
    elif isinstance(left, (str)):
        if isinstance(right, (date, datetime)):
            return left + str(right)
    elif isinstance(left, (date, datetime)):
        if isinstance(right, (str)):
            return str(left) + right
    lefttype = type(left).__name__
    righttype = type(right).__name__
    raise RuntimeError(f'no se puede dividir {lefttype} con {righttype}', position)

def castRelationalOperands(left, operator:str, right, position:tuple) -> tuple:
    if type(left) == date:
        if isinstance(right, str):
            try:
                right = date.fromisoformat(right)
            except ValueError:
                message = f'Operandos incompatibles para "{operator}". No se puede castear <{right}> de forma implicita'
                raise exceptions.RuntimeError(message, position)
    elif type(left) == datetime:
        if isinstance(right, str):
            try:
                right = datetime.fromisoformat(right)
            except ValueError:
                message = f'Operandos incompatibles para "{operator}". No se puede castear <{right}> de forma implicita'
                raise exceptions.RuntimeError(message, position)
    elif type(right) == date:
        if isinstance(left, str):
            try:
                left = date.fromisoformat(left)
            except ValueError:
                message = f'Operandos incompatibles para "{operator}". No se puede castear <{left}> de forma implicita'
                raise exceptions.RuntimeError(message, position)
    elif type(right) == datetime:
        if isinstance(left, str):
            try:
                left = datetime.fromisoformat(left)
            except ValueError:
                message = f'Operandos incompatibles para "{operator}". No se puede castear <{left}> de forma implicita'
                raise exceptions.RuntimeError(message, position)
    return (left, right)

def wrapInSymbol(key:str, value:Any, t:str, length:int|None=None) -> symbol.Symbol:
    if t == 'int':
        return symbol.Integer(key, value)
    elif t == 'decimal':
        return symbol.Decimal(key, value)
    elif t == 'nchar' or t == 'nvarchar':
        return symbol.VarChar(key, value, length)
    elif t == 'date':
        return symbol.Date(key, value)
    else:
        return symbol.DateTime(key, value)

def cast(value:str, t:str) -> Any:
    if t == 'int':
        return int(value)
    elif t == 'decimal':
        return float(value)
    else:
        return value

def printSignature(name:str, params:list):
    signature = ''
    for param in params:
        signature += str(param) + ', '
    return f'{name}({signature}) '
