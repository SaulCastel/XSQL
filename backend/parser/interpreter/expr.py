from typing import Any
from parser.interpreter.context import Context
from . import operations
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
            return left > right
        elif self.operator == '<':
            return left < right
        elif self.operator == '>=':
            return left >= right
        elif self.operator == '<=':
            return left <= right
        elif self.operator == '==' or self.operator == '=':
            return left == right
        elif self.operator == '!=':
            return left != right
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
