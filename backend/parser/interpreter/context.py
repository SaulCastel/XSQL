from typing import Any 
from typing_extensions import Self
from parser.interpreter.exceptions import RuntimeError
from parser.interpreter.symbol import Symbol

class Context:
    def __init__(self, prev:Self|None=None, name:str|None=None) -> None:
        self.prev = prev
        self.symbols:dict[str,Symbol] = {}
        self.name = name

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

    def dump(self) -> list[str]:
        symbols = []
        for key, symbol in self.symbols.items():
            symbols.append({
                'id':key,
                'type':symbol.__class__.__name__,
                'length':symbol.length,
                'value':symbol.__str__(),
                'where':self.name,
            })
        return symbols
