from . import operations

class Literal:
    def __init__(self, value, position) -> None:
        self.value = value
        self.position = position

    def interpret(self):
        return self.value

class Binary:
    def __init__(self, left, operator, right, position) -> None:
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position

    def interpret(self):
        left = self.left.interpret()
        right = self.right.interpret()
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
        elif self.operator == '==':
            return left == right
        elif self.operator == '!=':
            return left != right

class Unary:
    def __init__(self, operator, operand, position):
        self.operator = operator
        self.operand = operand
        self.position = position

    def interpret(self):
        if self.operator == '-':
            return - self.operand.interpret()
        elif self.operator == '!':
            return not self.operand.interpret()
