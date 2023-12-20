from typing import Any, Self
from parser.interpreter.exceptions import RuntimeError

class Symbol:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.t = self.value.__class__

    def update(self, value):
        '''
        Update Symbols's value.
        Raises RuntimeError on mismatching types
        '''
        if not isinstance(value, self.t):
            valueType = type(value).__name__
            raise RuntimeError(f'Simbolo {self.key} de tipo {self.t} no puede ser reasignado a tipo {valueType}')
        self.value = value

class Context:
    def __init__(self, prev:Self | None = None) -> None:
        self.prev = prev
        self.symbols = {}

    def declare(self, key: str, value: Any):
        '''Declare a new symbol in the current context/scope'''
        self.symbols[key] = Symbol(key, value)

    def set(self, key: str, value: Any):
        '''
        Search for a symbol on current context
        and all previous ones, then set its value
        '''
        symbol = self.get(key)
        symbol.update(value)

    def get(self, key: str) -> Symbol:
        '''
        Search for a symbol on current context
        and all previous ones
        '''
        symbol = self.symbols.get(key)
        if not symbol:
            if not self.prev:
                raise RuntimeError(f'No se reconoce {key} como un simbolo')
            symbol = self.prev.get(key)
        return symbol