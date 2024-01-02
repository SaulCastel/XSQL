from parser.interpreter.database import ddl,dml,ast
from parser.interpreter import expr, operations, exceptions, symbol
from parser.interpreter.context import Context
from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def interpret(self, context:Context, parserState:dict):
        pass
    def GenerarAST(self):
        pass

class Declare(Stmt):
    def __init__(self, key:str, t:str, length:int|None,contador:int):
        self.key = key
        self.t = t
        self.length = length
        self.contador = contador
    def interpret(self, context:Context, parserState:dict):
        newEntry = operations.wrapInSymbol(self.key, None, self.t, self.length)
        context.declare(self.key, newEntry)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="DECLARE"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        dot += f'"key{self.contador}" [label="{self.key} {self.t} "]\n'
        dot += f'"{self.contador}" -- "key{self.contador}" \n'
        
        return dot

class Set(Stmt):
    def __init__(self, key, expr, position,contador):
        self.key = key
        self.expr = expr
        self.position = position
        self.contador=contador
    def interpret(self, context: Context, parserState: dict):
        value = self.expr.interpret(context)
        context.set(self.key, value, self.position)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="SET"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        dot += f'"key{self.contador}" [label="{self.key}"]\n'
        dot += f'"{self.contador}" -- "key{self.contador}" \n'
        dot += f'"igual{self.contador}"[label=" = "]\n'
        dot += f'"{self.contador}" -- "igual{self.contador}" \n'
        dot += self.expr.GenerarAST()
        dot += f'"{self.contador}" -- "{self.expr.contador}" \n'
        return dot

class Select(Stmt):
    def __init__(self, exprs:list[tuple[expr.Expr,str]],contador:int) -> None:
        self.exprs = exprs
        self.contador = contador
    def interpret(self, context:Context, parserState:dict):
        header = []
        columns = []
        for expr in self.exprs:
            columns.append(expr[0].interpret(context))
            header.append(expr[1] if expr[1] else str(expr[0]))
        parserState['result'].append({'header':header, 'records':[columns]})
    
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="Select"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        for expr in self.exprs:
            dot += expr[0].GenerarAST()
            dot += f'"{self.contador}" -- "{expr[0].contador}" \n' 
        return dot
        

class SelectFrom(Stmt):
    def __init__(self, tableName, returnExprs, condition, position,contador):
        self.tableName = tableName
        self.returnExprs = returnExprs
        self.condition = condition
        self.position = position
        self.contador=contador

    def interpret(self, context:Context, parserState:dict):
        database = parserState['database']
        result = dml.selectFrom(context, database, self.tableName, self.returnExprs, self.condition, self.position)
        parserState['result'].append(result)

    def GenerarAST(self):
        dot = ast.selectFrom(self.tableName,self.returnExprs,self.condition,self.contador)
        return dot

class CreateBase(Stmt):
    def __init__(self, identifier,contador) -> None:
        self.identifier = identifier
        self.contador=contador

    def interpret(self, context: Context, parserState: dict):
        ddl.createBase(self.identifier)
    def GenerarAST(self):
        dot = ast.createBase(self.identifier,self.contador)
        return dot

class CreateTable(Stmt):
    def __init__(self,NameTable,column,contador) -> None:
        self.column=column
        self.NameTable =NameTable
        self.contador=contador
       
    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.createTable(self.NameTable, self.column, database)
    def GenerarAST(self):
        dot =ast.createTable(self.NameTable, self.column, self.contador)
        return dot

class DropTable(Stmt):
    def __init__(self, tableName:str, position:tuple,contador) -> None:
        self.tableName = tableName
        self.position = position
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.dropTable(database, self.tableName, self.position)
    
    def GenerarAST(self):
        dot = ast.dropTable(self.tableName,self.contador)
        return dot

class AlterADD(Stmt):
    def __init__(self,NameTable,column, position,contador) -> None:
        self.column=column
        self.NameTable =NameTable
        self.position = position
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterAdd(self.NameTable, self.column, database, self.position)
    
    def GenerarAST(self):
        dot = ast.alterAdd(self.NameTable, self.column,self.contador)
        return dot

class AlterDROP(Stmt):
    def __init__(self,NameTable,TextColumn, position,contador) -> None:
        self.TextColumn=TextColumn
        self.NameTable = NameTable
        self.position = position
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.alterDrop(self.NameTable, self.TextColumn, database, self.position)
    def GenerarAST(self):
        dot = ast.alterDrop(self.NameTable,self.TextColumn,self.contador)
        return dot
class Insert(Stmt):
    def __init__(self, table, selection, values, position,contador):
        self.table = table
        self.selection = selection
        self.values = values
        self.position = position
        self.contador= contador

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        dml.insert(context, database, self.table, self.selection, self.values, self.position)
    def GenerarAST(self):
        dot = ast.insert(self.table,self.selection,self.values,self.contador)
        return dot
class Usar(Stmt): 
    def __init__(self,uso,contador) -> None:
        self.uso = uso
        self.contador=contador
    
    def interpret(self, context: Context, parserState: dict):
        parserState['database'] = self.uso
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="USAR"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        dot += f'"identificador{self.contador}" [label="{self.uso}"]\n'
        dot += f'"{self.contador}" -- "identificador{self.contador}"'
        return dot

class Truncate(Stmt):
    def __init__(self,identifier, position,contador) -> None:
        self.identifier=identifier
        self.position = position
        self.contador =contador

    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        ddl.truncate(self.identifier,database, self.position)

    def GenerarAST(self):
        dot = ast.truncate(self.identifier,self.contador)
        return dot

class Delete(Stmt):
    def __init__(self,identifier,condition,position,contador)-> None:
        self.identifier=identifier
        self.condition=condition
        self.position=position
        self.contador= contador
    def interpret(self, context: Context, parserState: dict):
        database = parserState['database']
        dml.delete(context,database,self.identifier,self.condition,self.position)
    def GenerarAST(self):
        dot =ast.delete(self.identifier,self.condition,self.contador)
        return dot 

class Update(Stmt):
    def __init__(self,identifier,list,condition,contador):
        self.identifier=identifier
        self.list=list
        self.condition= condition
        self.contador = contador
    def interpret(self, context: Context, parserState: dict):
        database=parserState['database']
        dml.update(context,database,self.identifier,self.condition,self.list)
    def GenerarAST(self):
        dot = ast.update(self.identifier,self.condition,self.list,self.contador)
        return dot
class Block(Stmt):
    def __init__(self, stmts:list[Stmt],contador:int) -> None:
        self.stmts = stmts
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        if parserState:
            parserState['block'] += 1
            context.name += f' Bloque {parserState["block"]}'
        for stmt in self.stmts:
            stmt.interpret(context, parserState)
        if parserState:
            parserState['symbols'].extend(context.dump())

    def GenerarAST(self):
        dot = f'"{self.contador}" [label="Stmts"]\n'
        
        ins = self.stmts
        for a in range(len(ins)):
            dot += f'"{self.contador}" -- "stmt{ins[a].contador}"\n'
            
            dot += ins[a].GenerarAST()
        return dot

class Ciclo_while(Stmt):
    def __init__(self,expresion:expr.Expr,listStmt:Block,contador:int):
        self.expresion=expresion
        self.listStmt=listStmt
        self.contador = contador
    def interpret(self, context: Context, parserState: dict):
        WhileContext = Context(context, 'While')
        while self.expresion.interpret(context):
            self.listStmt.interpret(WhileContext,parserState)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="WHILE"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        dot += self.expresion.GenerarAST()
        dot += f'"{self.contador}" -- "{self.expresion.contador}" \n'
        dot += self.listStmt.GenerarAST()
        dot += f'"{self.contador}" -- "{self.listStmt.contador}" \n'
        
        return dot

class Ssl_IF(Stmt):
    def __init__(self,expresion:expr.Expr,trueBlock:Block,falseBlock:Block|None,contador:int):
        self.expresion=expresion
        self.trueBlock=trueBlock
        self.falseBlock=falseBlock
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        if self.expresion.interpret(context):
            IfContext = Context(context, 'If')
            self.trueBlock.interpret(IfContext, parserState)
        else:
            if self.falseBlock:
                ElseContext = Context(context, 'Else')
                self.falseBlock.interpret(ElseContext, parserState)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="IF"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        dot += self.expresion.GenerarAST()
        dot += f'"{self.contador}" -- "{self.expresion.contador}" \n'
        dot += self.trueBlock.GenerarAST()
        dot += f'"{self.contador}" -- "{self.trueBlock.contador}" \n'
        if self.falseBlock:
            dot += f'"else{self.contador}" [label="ELSE"]\n'
            dot += f'"{self.contador}" -- "else{self.contador}" \n'
            dot += self.falseBlock.GenerarAST()
            dot += f'"else{self.contador}" -- "{self.falseBlock.contador}" \n'    
        return dot

class Ssl_Case(Stmt):
    def __init__(self, ListWhen:list[tuple[expr.Expr, Stmt]], ElseOptions:Stmt,contador:int):
        self.ListWhen=ListWhen
        self.ElseOptions=ElseOptions
        self.contador=contador

    def interpret(self, context: Context, parserState: dict):
        for Element in self.ListWhen:
            if not Element[0].interpret(context):
                continue
            Element[1].interpret(context,parserState)     
            break
        else:
            self.ElseOptions.interpret(context, parserState)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="CASE"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        numero=0
        for Element in self.ListWhen:
            dot += f'"when{self.contador}_{numero}" [label="WHEN"]\n'
            dot += f'"{self.contador}" -- "when{self.contador}_{numero}" \n'
            dot += Element[0].GenerarAST()
            dot += f'"when{self.contador}_{numero}" -- "{Element[0].contador}" \n'
            dot += f'"then{self.contador}_{numero}" [label="THEN"]\n'
            dot += f'"when{self.contador}_{numero}" -- "then{self.contador}_{numero}" \n'
            dot += Element[1].GenerarAST()
            dot += f'"then{self.contador}_{numero}" -- "stmt{Element[1].contador}" \n'
            numero+=1
        dot += f'"else{self.contador}" [label="ELSE"]\n'
        dot += f'"{self.contador}" -- "else{self.contador}" \n'
        dot += f'"then{self.contador}" [label="THEN"]\n'
        dot += f'"else{self.contador}" -- "then{self.contador}" \n'
        dot += self.ElseOptions.GenerarAST()
        dot += f'"then{self.contador}" -- "stmt{self.ElseOptions.contador}" \n'
        return dot

class CreateProc(Stmt):
    def __init__(self, key:str, params:list, stmts:Block,contador) -> None:
        self.key = key
        self.params = params
        self.stmts = stmts
        self.contador= contador

    def interpret(self, context: Context, parserState: dict):
        newProc = symbol.Proc(self.key, self.params, self.stmts)
        context.declare(f'{self.key}', newProc)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="PROCEDURE"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        if self.stmts:
            dot += f'"else{self.contador}" [label="ELSE"]\n'
            dot += f'"{self.contador}" -- "else{self.contador}" \n'
            dot += self.stmts.GenerarAST()
            dot += f'"else{self.contador}" -- "{self.stmts.contador}" \n'    
        return dot

class ExecProc(Stmt):
    def __init__(self, key:str, args:list[expr.Expr], position:tuple,contador) -> None:
        self.key = key
        self.args = args
        self.position = position
        self.contador= contador

    def interpret(self, context: Context, parserState: dict):
        proc:symbol.Callable = context.get(self.key, self.position)
        paramsLength = len(proc.params)
        argsLength = len(self.args)
        if paramsLength != argsLength:
            msg = f'Disparidad en argumentos para {self.key}, se esperaban {paramsLength}, se obtuvieron {argsLength}'
            raise exceptions.RuntimeError(msg, self.position)
        procContext = Context(context, f'{self.key}')
        for i in range(len(self.args)):
            key = proc.params[i][0]
            argType = proc.params[i][1][0]
            length = proc.params[i][1][1]
            value = self.args[i].interpret(context)
            if length:
                length = int(length)
            sym = operations.wrapInSymbol(key, value, argType, length)
            procContext.declare(key, sym)
        proc.block.interpret(procContext, parserState)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="FUNCTION"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        return dot

class CreateFunc(Stmt):
    def __init__(self, key:str, params:list, returnType:tuple, stmts:Block,contador:int) -> None:
        self.key = key
        self.params = params
        self.returnType = returnType
        self.stmts = stmts
        self.contador= contador

    def interpret(self, context: Context, parserState: dict):
        newFunc = symbol.Func(self.key, self.params, self.returnType, self.stmts)
        context.declare(f'{self.key}', newFunc)
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="FUNCTION"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        if self.stmts:
            dot += f'"else{self.contador}" [label="ELSE"]\n'
            dot += f'"{self.contador}" -- "else{self.contador}" \n'
            dot += self.stmts.GenerarAST()
            dot += f'"else{self.contador}" -- "{self.stmts.contador}" \n'    
        return dot

class Return(Stmt):
    def __init__(self, expr:expr.Expr,contador) -> None:
        self.expr = expr
        self.contador = contador

    def interpret(self, context: Context, parserState: dict):
        raise exceptions.Return(self.expr.interpret(context))
    def GenerarAST(self):
        dot = f'"stmt{self.contador}" [label="stmt"]\n'
        dot += f'"{self.contador}" [label="RETURN"]\n'
        dot += f'"stmt{self.contador}" -- "{self.contador}" \n'
        return dot