from parser.interpreter.context import Context
from parser.interpreter.symbol import Symbol
from parser.interpreter import stmt
from parser.interpreter import operations

def Create_procedure(context:Context, identifier:str, parameters:list, instructions:stmt, parserState:dict):
    localContext = Context(context)
    for param in parameters:
        localContext.declare(identifier,operations.wrapInSymbol(param[0], param[1], None),instructions)

def Exec_procedure():
    print("Hola")
    # for stmt in instructions:
    #     stmt.interpret(localContext,parserState)
    
def Create_function(context:Context, identifier:str, parameters:list, returnType:str, instructions:stmt, parserState:dict):
    localContext = Context(context)
    localSymbol = {}
    for param in parameters:
        localSymbol[param[0]] = (operations.wrapInSymbol(param[0], param[1], None))
    localSymbol["return"] = (operations.wrapInSymbol("return", returnType, None))
    localContext.declare(identifier,localSymbol,instructions)
    for stmt in instructions:
        stmt.interpret(localContext,parserState)
        
def Call_function():
    print("Adios")
