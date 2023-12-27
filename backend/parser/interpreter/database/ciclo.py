from . import common
from parser.interpreter.context import Context
from parser.interpreter import expr
from parser.interpreter import stmt

def ciclo_while(context:Context,expresion:expr.Binary,intrrucciones: stmt, parserState:dict):
    
    WhileContext = Context(context)

    while expresion.interpret(context):
        for stmt in intrrucciones:
                stmt.interpret(WhileContext,parserState)

def ssl_If(context:Context,expresion:expr.Binary,insrucciones:stmt,instruccionesElse:stmt,parserState:dict):
     IfContext = Context(context)

     if expresion.interpret(context):
          for stmt in insrucciones:
               stmt.interpret(IfContext,parserState)
     else:
          if instruccionesElse != None:
               for stmt in instruccionesElse:
                    stmt.interpret(IfContext,parserState)

def ssl_Case(context:Context,ListWhen:list ,ElseOptions:expr or stmt, FinCase:str, parserState:dict):

     if FinCase != None:
          for Element in ListWhen:
               if Element[0].interpret(context):
                    Element[1].interpret(context,parserState)     
     else:
          print ("FinCase",FinCase)

          