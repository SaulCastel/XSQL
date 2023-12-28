from typing import Any
from parser.interpreter.context import Context
from . import operations
from parser.interpreter import exceptions
from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def interpret(self, context:Context) -> Any:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Literal(Expr):
    def __init__(self, value, position) -> None:
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return str(self.value)

    def interpret(self, context:Context):
        return self.value

class Binary(Expr):
    def __init__(self, left, operator, right, position) -> None:
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position

    def __str__(self) -> str:
        return f'{self.left} {self.operator} {self.right} '

    def interpret(self, context:Context):
        left = self.left.interpret(context)
        right = self.right.interpret(context)
        if self.operator == '+':
            return operations.sum(left, right, self.position)
        elif self.operator == '-':
            return operations.sub(left, right, self.position)
        elif self.operator == '*':
            return operations.mult(left, right, self.position)
        elif self.operator == '/':
            return operations.div(left, right, self.position)
        elif self.operator == '>':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] > operands[1]
        elif self.operator == '<':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] < operands[1]
        elif self.operator == '>=':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] >= operands[1]
        elif self.operator == '<=':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] <= operands[1]
        elif self.operator == '==' or self.operator == '=':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] == operands[1]
        elif self.operator == '!=':
            operands = operations.castRelationalOperands(left, self.operator, right, self.position)
            return operands[0] != operands[1]
        elif self.operator == '&&':
            return left and right
        elif self.operator == '||':
            return left or right

class Unary(Expr):
    def __init__(self, operator, operand, position):
        self.operator = operator
        self.operand = operand
        self.position = position

    def __str__(self) -> str:
        return f'{self.operator} {self.operand} '

    def interpret(self, context:Context):
        if self.operator == '-':
            return - self.operand.interpret(context)
        elif self.operator == '!':
            return not self.operand.interpret(context)

class Symbol(Expr):
    def __init__(self, key:str, position:tuple) -> None:
        self.key = key
        self.position = position

    def __str__(self) -> str:
        return self.key

    def interpret(self, context:Context):
        return context.get(self.key, self.position).value

class Between(Expr):
    def __init__(self, symbol:Expr, min:Expr, max:Expr, position:tuple) -> None:
        self.symbol = symbol
        self.min = min
        self.max = max
        self.position = position

    def __str__(self) -> str:
        return f'{self.symbol} between {self.min} and {self.max} '

    def interpret(self, context: Context) -> Any:
        minCheck = Binary(self.symbol, '>=', self.min, self.position)
        maxCheck = Binary(self.symbol, '<=', self.max, self.position)
        if minCheck.interpret(context) and maxCheck.interpret(context):
            return True
        return False

class Concatenar(Expr):
    def __init__(self, exprs:list[Expr], position:tuple) -> None:
        self.exprs = exprs
        self.position = position

    def __str__(self) -> str:
        return operations.printSignature('concatenar', self.exprs)

    def interpret(self, context:Context):
        if len(self.exprs) < 2:
            raise exceptions.RuntimeError('no. de argumentos invalido', self.position)
        concat = self.exprs[0]
        for i in range(1, len(self.exprs)):
            concat = Binary(concat, '+', self.exprs[i], self.position)
        return concat.interpret(context)

class Substaer(Expr):
    def __init__(self, exprs:list[Expr], position:tuple) -> None:
        self.exprs = exprs
        self.position = position
    
    def __str__(self) -> str:
        return operations.printSignature('substraer', self.exprs)

    def interpret(self, context:Context):
        if len(self.exprs) != 3:
            raise exceptions.RuntimeError('no. de argumentos invalido', self.position)
        cadena = self.exprs[0].interpret(context)
        inicio = self.exprs[1].interpret(context)
        longitud = self.exprs[2].interpret(context)
        if isinstance(cadena, str) and isinstance(inicio, int) and isinstance(longitud, int):
            return cadena[inicio-1:inicio-1+longitud]
        else:
            raise exceptions.RuntimeError("los parametros deben ser (str,int,int)", self.position)

class Hoy(Expr):
    def __str__(self) -> str:
        return 'hoy() '

    def interpret(self, context:Context):
        from datetime import datetime

        fecha_hora_actual = datetime.now()
        
        formato_personalizado = "%Y-%m-%d %H:%M:%S"
        fecha_hora_formateada = fecha_hora_actual.strftime(formato_personalizado)

        return fecha_hora_formateada

class Contar:
    def __init__(self, selection:str|Symbol, position:tuple) -> None:
        self.selection = selection
        self.position = position

    def __str__(self) -> str:
        return f'contar({self.selection}) '

    def interpret(self, records:list[Context]) -> Any:
        if self.selection == '*':
            return len(records)
        count = 0
        for record in records:
            cell = record.get(self.selection.key, self.position)
            if cell.value:
                count += 1
        return count

class Sumar:
    def __init__(self, selection:Symbol, position:tuple) -> None:
        self.selection = selection
        self.position = position

    def __str__(self) -> str:
        return f'sumar({self.selection}) '

    def interpret(self, records:list[Context]) -> Any:
        sum = 0
        for record in records:
            cell = record.get(self.selection.key, self.position)
            if cell.value:
                sum += cell.value
        return sum
