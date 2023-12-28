from parser.interpreter.database import ddl,dml,ciclo
from parser.interpreter import expr, operations
from parser.interpreter.context import Context
from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def interpret(self, context:Context, parserState:dict):
        pass

class Declare(Stmt):
    def __init__(self, key:str, t:str, length:int|None):
        self.key = key
        self.t = t
        self.length = length

    def interpret(self, context:Context, parserState:dict):
        newEntry = operations.wrapInSymbol(self.key, None, self.t, self.length)
        context.declare(self.key, newEntry)

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

class DropTable(Stmt):
    def __init__(self, tableName:str, position:tuple) -> None:
        self.tableName = tableName
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.dropTable(database, self.tableName, self.position)

class AlterADD(Stmt):
    def __init__(self,NameTable,column, position) -> None:
        self.column=column
        self.NameTable =NameTable
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterAdd(self.NameTable, self.column, database, self.position)

class AlterDROP(Stmt):
    def __init__(self,NameTable,TextColumn, position) -> None:
        self.TextColumn=TextColumn
        self.NameTable =NameTable
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterDrop(self.NameTable, self.TextColumn, database, self.position)

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

class Truncate(Stmt):
    def __init__(self,identifier, position) -> None:
        self.identifier=identifier
        self.position = position

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.truncate(self.identifier,database, self.position)

class Delete(Stmt):
    def __init__(self,identifier,condition,position)-> None:
        self.identifier=identifier
        self.condition=condition
        self.position=position
    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        dml.delete(context,database,self.identifier,self.condition,self.position)

class Update(Stmt):
    def __init__(self,identifier,list,condition):
        self.identifier=identifier
        self.list=list
        self.condition= condition
    def interpret(self, context: Context, parserState: dict):
        database=parserState['database']
        dml.update(context,database,self.identifier,self.condition,self.list)

class Ciclo_while(Stmt):
    def __init__(self,expresion,listStmt):
        self.expresion=expresion
        self.listStmt=listStmt
    def interpret(self, context: Context, parserState: dict):
        ciclo.ciclo_while(context,self.expresion,self.listStmt,parserState)

class Ssl_IF(Stmt):
    def __init__(self,expresion,listStmt,listStmtElse):
        self.expresion=expresion
        self.listStmt=listStmt
        self.listStmtElse=listStmtElse
    def interpret(self, context: Context, parserState: dict):
        ciclo.ssl_If(context,self.expresion,self.listStmt,self.listStmtElse,parserState)

class Ssl_Case(Stmt):
    def __init__(self,ListWhen,ElseOptions,FinCase):
        self.ListWhen=ListWhen
        self.ElseOptions=ElseOptions
        self.FinCase=FinCase
    def interpret(self, context: Context, parserState: dict):
        ciclo.ssl_Case(context,self.ListWhen,self.ElseOptions,self.FinCase,parserState)
