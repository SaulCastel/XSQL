class Binary:
    def __init__(self, left, operator, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def interpret(self):
        if self.operator == '+':
            return self.left.interpret() + self.right.interpret()
        elif self.operator == '-':
            return self.left.interpret() - self.right.interpret()
        elif self.operator == '*':
            return self.left.interpret() * self.right.interpret()
        elif self.operator == '/':
            return self.left.interpret() / self.right.interpret()

class Unary:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def interpret(self):
        if self.operator == '-':
            return - self.operand.interpret()
        elif self.operator == '!':
            return not self.operand.interpret()

class Literal:
    def __init__(self, lexeme, type) -> None:
        self.lexeme = lexeme
        self.type = type

    def interpret(self):
        if self.type == 'int':
            return int(self.lexeme)
        elif self.type == 'decimal':
            return float(self.lexeme)
