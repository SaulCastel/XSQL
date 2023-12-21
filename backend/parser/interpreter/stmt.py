from parser.interpreter import expr
from parser.interpreter.database import ddl, dml
from parser.interpreter.context import Context
from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def interpret(self, context:Context, parserState:dict):
        pass

class Declare(Stmt):
    def __init__(self, key, t, length=None):
        self.key = key
        self.t = t
        self.length = length

    def interpret(self, context:Context, parserState:dict):
        context.declare(self.key, None, self.t, self.length)

class Set(Stmt):
    def __init__(self, key, expr, position):
        self.key = key
        self.expr = expr
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        value = self.expr.interpret(context)
        context.set(self.key, value, self.position)

class Select(Stmt):
    def __init__(self, exprs:list[tuple[expr.Expr,str]]) -> None:
        self.exprs = exprs

    def interpret(self, context:Context, parserState:dict):
        header = []
        columns = []
        for expr in self.exprs:
            columns.append(expr[0].interpret(context))
            header.append(expr[1] if expr[1] else str(expr[0]))
        parserState['result'].append({'header':header, 'records':[columns]})

class SelectFrom(Stmt):
    def __init__(self, tableName, returnExprs, condition, position):
        self.tableName = tableName
        self.returnExprs = returnExprs
        self.condition = condition
        self.position = position

    def interpret(self, context:Context, parserState:dict):
        database = parserState['database']
        result = dml.selectFrom(context, database, self.tableName, self.returnExprs, self.condition, self.position)
        parserState['result'].append(result)

class CreateBase(Stmt):
    def __init__(self, identifier) -> None:
        self.identifier = identifier

    def interpret(self, context: Context, parserState: dict):
        ddl.createBase(self.identifier)

class CreateTable(Stmt):
    def __init__(self,NameTable,column) -> None:
        self.column=column
        self.NameTable =NameTable
       
    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.createTable(self.NameTable, self.column, database)

class AlterADD(Stmt):
    def __init__(self,NameTable,column) -> None:
       self.column=column
       self.NameTable =NameTable

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterAdd(self.NameTable, self.column, database)

class AlterDROP(Stmt):
    def __init__(self,NameTable,TextColumn) -> None:
       self.TextColumn=TextColumn
       self.NameTable =NameTable

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterDrop(self.NameTable, self.TextColumn, database)

class Insert(Stmt):
    def __init__(self, table, selection, values, position):
        self.table = table
        self.selection = selection
        self.values = values
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        dml.insert(context, database, self.table, self.selection, self.values, self.position)

class Usar(Stmt): 
    def __init__(self,uso) -> None:
        self.uso = uso
    
    def interpret(self, context: Context, parserState: dict):
        parserState['database'] = self.uso
