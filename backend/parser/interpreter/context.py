from typing import Any 
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter.symbol import Symbol

class Symbol:
    def __init__(self, key: str, value: Any, t:Any):
        self.key = key
        self.value = value
        self.t = t

    def update(self, value):
        '''
        Update Symbols's value.
        Raises RuntimeError on mismatching types
        '''
#        if not isinstance(value, self.t):
#            valueType = type(value).__name__
#            raise RuntimeError(f'Simbolo {self.key} de tipo {self.t} no puede ser reasignado a tipo {valueType}')
        self.value = value




class Context:
    def __init__(self, prev = None) -> None:
        self.prev = prev
        self.symbols:dict[str,Symbol] = {}

    def declare(self, key: str, value: Symbol):
        '''Declare a new symbol in the current context/scope'''
        self.symbols[key] = value

    def set(self, key: str, value: Any, position:tuple):
        '''
        Search for a symbol on current context
        and all previous ones, then set its value.
        key must exist, or RuntimeError is raised.
        *Use Context.declare to create a new entry instead.
        '''
        symbol = self.get(key, position)
        symbol.update(value)

    def get(self, key: str, position:tuple|None) -> Symbol:
        '''
        Search for a symbol on current context
        and all previous ones
        '''
        symbol = self.symbols.get(key)
        if not symbol:
            if not self.prev:
                raise RuntimeError(f'No se reconoce {key} como un simbolo', position)
            symbol = self.prev.get(key, position)
        return symbol
