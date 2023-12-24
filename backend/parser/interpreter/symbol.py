from abc import ABC, abstractmethod
from datetime import date, datetime
from types import NoneType
from typing import Any

class Symbol(ABC):
    def __init__(self, key:str, t:Any):
        self.key = key
        self.t = t
        self.value = None

    @abstractmethod
    def update(self, value:Any) -> None:
        '''
        Update Symbols's value.
        Raises RuntimeError on mismatching types
        '''

    def matchType(self, value:Any) -> None:
        if value == None:
            return
        if not isinstance(value, self.t):
            valueType = type(value).__name__
            raise RuntimeError(f'Simbolo {self.key} de tipo: {self.t.__name__} no puede ser asignado a tipo: {valueType}')

class VarChar(Symbol):
    def __init__(self, key:str, value:str|None, length:int):
        super().__init__(key, str)
        self.length = length
        self.update(value)

    def __str__(self) -> str:
        if not self.value:
            return str(self.value)
        return self.value

    def update(self, value:str|None) -> None:
        self.matchType(value)
        if value and len(value) > self.length:
            self.value = value[0:self.length]
        else:
            self.value = value

class Integer(Symbol):
    def __init__(self, key:str, value:int|None):
        super().__init__(key, int)
        self.update(value)

    def __str__(self) -> str:
        return str(self.value)

    def update(self, value:int|None) -> None:
        self.matchType(value)
        self.value = value

class Decimal(Symbol):
    def __init__(self, key:str, value:float|None):
        super().__init__(key, float)
        self.update(value)

    def __str__(self) -> str:
        return str(self.value)

    def update(self, value:float|None) -> None:
        self.matchType(value)
        self.value = value

class Date(Symbol):
    def __init__(self, key:str, value:date|None):
        super().__init__(key, date)
        self.update(value)

    def __str__(self) -> str:
        if not self.value:
            return str(self.value)
        return self.value.strftime('%d-%m-%Y')

    def update(self, value:date|None) -> None:
        self.matchType(value)
        self.value = value

class DateTime(Symbol):
    def __init__(self, key:str, value:datetime|None):
        super().__init__(key, datetime)
        self.update(value)

    def __str__(self) -> str:
        if not self.value:
            return str(self.value)
        return self.value.strftime('%d-%m-%Y %H:%M:%S')

    def update(self, value:datetime|None) -> None:
        self.matchType(value)
        self.value = value
