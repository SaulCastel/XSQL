from . import common
from parser.interpreter.context import Context
from parser.interpreter import expr
from parser.interpreter import stmt

def ciclo_while(context:Context,expresion:expr.Binary,intrrucciones: stmt, parserState:dict):
    
    WhileContext = Context(context)

    while expresion.interpret(context):
        for stmt in intrrucciones:
                stmt.interpret(WhileContext,parserState)

def ssl_If(context:Context,expresion:expr.Binary,insrucciones:stmt,parserState:dict):
     IfContext = Context(context)

     if expresion.interpret(context):
          for stmt in insrucciones:
               stmt.interpret(IfContext,parserState)
def ssl_Case(context:Context,ListWhen:list ,ElseOptions:expr or stmt, FinCase:str, parserState:dict):
     print("Lista when",ListWhen)
     print("Option Else",ElseOptions)
     print("finCase",FinCase)


          