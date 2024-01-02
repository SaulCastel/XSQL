from typing import Any
from parser.interpreter.context import Context
from parser.interpreter import symbol
from . import operations
from parser.interpreter import exceptions
from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def interpret(self, context:Context) -> Any:
        pass
    def GenerarAST(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Literal(Expr):
    def __init__(self, value, position,contador) -> None:
        self.value = value
        self.position = position
        self.contador =contador
    def __str__(self) -> str:
        return str(self.value)

    def interpret(self, context:Context):
        return self.value
    def GenerarAST(self):
        dot = f'"{self.contador}"[label ="expr"]\n'
        dot += f'"valor{self.contador}"[label ="{self.value}"]\n'
        dot += f'"{self.contador}" -- "valor{self.contador}" \n'
        return dot

class Binary(Expr):
    def __init__(self, left, operator, right, position,contador) -> None:
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position
        self.contador = contador

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
        
    def GenerarAST(self):
        dot =""
        dot += self.left.GenerarAST()
        dot += self.right.GenerarAST()
        dot += f'"{self.contador}"[label ="expr"]\n'
        dot += f'"realiza{self.contador}"[label ="{self.operator}"]\n'
        dot += f'"{self.contador}"--"{self.left.contador}"\n'
        dot += f'"{self.contador}"--"realiza{self.contador}"\n'
        dot += f'"{self.contador}"--"{self.right.contador}"\n'
        return dot

class Unary(Expr):
    def __init__(self, operator, operand, position,contador):
        self.operator = operator
        self.operand = operand
        self.position = position
        self.contador = contador

    def __str__(self) -> str:
        return f'{self.operator} {self.operand} '

    def interpret(self, context:Context):
        if self.operator == '-':
            return - self.operand.interpret(context)
        elif self.operator == '!':
            return not self.operand.interpret(context)
    def GenerarAST(self): 
        dot = f'"{self.contador}"[label ="expr"]\n'
        
        if self.operator == '-':
            dot += f'"operator{self.contador}"[label =" - "]\n'
            dot += self.operand.GenerarAST()
            dot += f'"operator{self.contador}" -- "{self.operand.contador}" \n'
        elif self.operator == '!':
            dot += f'"operator{self.contador}"[label =" ! "]\n'
            dot += self.operand.GenerarAST()
            dot += f'"operator{self.contador}" -- "{self.operand.contador}" \n'
        dot += f'"{self.contador}" -- "operator{self.contador}" \n'
        return dot

class Symbol(Expr):
    def __init__(self, key:str, position:tuple,contador) -> None:
        self.key = key
        self.position = position
        self.contador = contador

    def __str__(self) -> str:
        return self.key

    def interpret(self, context:Context):
        return context.get(self.key, self.position).value
    def GenerarAST(self): 
        dot = f'"{self.contador}"[label ="expr"]\n'
        dot += f'"valor{self.contador}"[label ="{self.key}"]\n'
        dot += f'"{self.contador}" -- "valor{self.contador}" \n'
        return dot
        

class Between(Expr):
    def __init__(self, symbol:Expr, min:Expr, max:Expr, position:tuple,contador:int) -> None:
        self.symbol = symbol
        self.min = min
        self.max = max
        self.position = position
        self.contador = contador

    def __str__(self) -> str:
        return f'{self.symbol} between {self.min} and {self.max} '

    def interpret(self, context: Context) -> Any:
        minCheck = Binary(self.symbol, '>=', self.min, self.position,self.contador)
        maxCheck = Binary(self.symbol, '<=', self.max, self.position,self.contador)
        if minCheck.interpret(context) and maxCheck.interpret(context):
            return True
        return False
    
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="BETWEEN"]\n'
        dot += self.min.GenerarAST() 
        dot += f'"{self.contador}" -- "{self.min.contador}" \n'
        dot += f'"and{self.contador}" [label="&&"]\n'
        dot += f'"{self.contador}" -- "and{self.contador}" \n'
        dot += self.max.GenerarAST()
        dot += f'"{self.contador}" -- "{self.max.contador}" \n'
        return dot

class Concatenar(Expr):
    def __init__(self, exprs:list[Expr], position:tuple,contador:int) -> None:
        self.exprs = exprs
        self.position = position
        self.contador = contador

    def __str__(self) -> str:
        return operations.printSignature('concatenar', self.exprs)

    def interpret(self, context:Context):
        if len(self.exprs) < 2:
            raise exceptions.RuntimeError('no. de argumentos invalido', self.position)
        concat = ''
        for e in self.exprs:
            concat += str(e.interpret(context))
        return concat
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="CONCATENAR"]\n'
        
        for Expr in self.exprs:
            dot += Expr.GenerarAST()
            dot += f'"{self.contador}" -- "{Expr.contador}" \n'
        return dot

class Substaer(Expr):
    def __init__(self, exprs:list[Expr], position:tuple,contador) -> None:
        self.exprs = exprs
        self.position = position
        self.contador = contador
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
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="SUBSTRAER"]\n'
        for Expr in self.exprs:
            dot += Expr.GenerarAST()
            dot += f'"{self.contador}" -- "{Expr.contador}" \n'
        return dot
        
class Hoy(Expr):
    def __init__(self,contador:int) -> None:
        self.contador = contador

    def __str__(self) -> str:
        return 'hoy() '

    def interpret(self, context:Context):
        from datetime import datetime

        fecha_hora_actual = datetime.now()
        
        formato_personalizado = "%Y-%m-%d %H:%M:%S"
        fecha_hora_formateada = fecha_hora_actual.strftime(formato_personalizado)

        return fecha_hora_formateada
    
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="HOY"]\n'
        return dot

class Contar:
    def __init__(self, selection:str|Symbol, position:tuple,contador:int) -> None:
        self.selection = selection
        self.position = position
        self.contador = contador

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
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="CONTAR"]\n'
        dot += f'"selection{self.contador}" [label="{self.selection}"]\n'
        dot += f'"{self.contador}" -- "selection{self.contador}" \n'
        return dot

class Sumar:
    def __init__(self, selection:Symbol, position:tuple,contador) -> None:
        self.selection = selection
        self.position = position
        self.contador = contador

    def __str__(self) -> str:
        return f'sumar({self.selection}) '

    def interpret(self, records:list[Context]) -> Any:
        sum = 0
        for record in records:
            cell = record.get(self.selection.key, self.position)
            if cell.value:
                sum += cell.value
        return sum
    
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="SUMAR"]\n'
        dot += f'"selection{self.contador}" [label="{self.selection}"]\n'
        dot += f'"{self.contador}" -- "selection{self.contador}" \n'
        return dot

class If(Expr):
    def __init__(self, condition:Expr, trueExpr:Expr, falseExpr:Expr) -> None:
        self.condition = condition
        self.trueExpr = trueExpr
        self.falseExpr = falseExpr

    def __str__(self) -> str:
        return f'if({self.condition}, {self.trueExpr}, {self.falseExpr})'

    def interpret(self, context: Context) -> Any:
        if self.condition.interpret(context):
            return self.trueExpr.interpret(context)
        return self.falseExpr.interpret(context)

class Case(Expr):
    def __init__(self, cases:list[tuple[Expr, Expr]], default:Expr, alias:str,contador:int) -> None:
        self.cases = cases
        self.default = default
        self.alias = alias
        self.contador= contador
    def __str__(self) -> str:
        return self.alias

    def interpret(self, context: Context) -> Any:
        for case in self.cases:
            if not case[0].interpret(context):
                continue
            return case[1].interpret(context)
        return self.default.interpret(context)
    
    def GenerarAST(self):
        dot = f'"{self.contador}" [label="CASE"]\n'
        numero=0
        for Element in self.cases:
            dot += f'"when{self.contador}_{numero}" [label="WHEN"]\n'
            dot += f'"{self.contador}" -- "when{self.contador}_{numero}" \n'
            dot += Element[0].GenerarAST()
            dot += f'"when{self.contador}_{numero}" -- "{Element[0].contador}" \n'
            dot += f'"then{self.contador}_{numero}" [label="THEN"]\n'
            dot += f'"when{self.contador}_{numero}" -- "then{self.contador}_{numero}" \n'
            dot += Element[1].GenerarAST()
            dot += f'"then{self.contador}_{numero}" -- "{Element[1].contador}" \n'
            numero+=1
        dot += f'"else{self.contador}" [label="ELSE"]\n'
        dot += f'"{self.contador}" -- "else{self.contador}" \n'
        dot += f'"then{self.contador}" [label="THEN"]\n'
        dot += f'"else{self.contador}" -- "then{self.contador}" \n'
        dot += self.default.GenerarAST()
        dot += f'"then{self.contador}" -- "{self.default.contador}" \n'
        return dot

class CallFunc(Expr):
    def __init__(self, key:str, args:list, position:tuple) -> None:
        self.key = key
        self.args = args
        self.position = position

    def __str__(self) -> str:
        return operations.printSignature(self.key, self.args)

    def interpret(self, context: Context) -> Any:
        func:symbol.Callable = context.get(self.key, self.position)
        paramsLength = len(func.params)
        argsLength = len(self.args)
        if paramsLength != argsLength:
            msg = f'Disparidad en argumentos para {self.key}, se esperaban {paramsLength}, se obtuvieron {argsLength}'
            raise exceptions.RuntimeError(msg, self.position)
        funcContext = Context(context, f'{self.key}')
        for i in range(len(self.args)):
            key = func.params[i][0]
            argType = func.params[i][1][0]
            length = func.params[i][1][1]
            value = self.args[i].interpret(context)
            if length:
                length = int(length)
            sym = operations.wrapInSymbol(key, value, argType, length)
            funcContext.declare(key, sym)
        return func.block.interpret(funcContext)
