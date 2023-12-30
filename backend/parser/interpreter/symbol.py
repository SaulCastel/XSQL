from parser.interpreter import exceptions
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any

class Symbol(ABC):
    def __init__(self, key:str, t:Any):
        self.key = key
        self.t = t
        self.value = None
        self.length = None

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
            raise RuntimeError(f'Simbolo {self.key} de tipo: {self.t} no puede ser asignado a tipo: {valueType}')

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
    def __init__(self, key:str, value:int|float|None):
        super().__init__(key, (int, float))
        self.update(value)

    def __str__(self) -> str:
        return str(self.value)

    def update(self, value:int|float|None) -> None:
        self.matchType(value)
        self.value = value

class Decimal(Symbol):
    def __init__(self, key:str, value:float|int|None):
        super().__init__(key, (float, int))
        self.update(value)

    def __str__(self) -> str:
        return str(self.value)

    def update(self, value:float|int|None) -> None:
        self.matchType(value)
        self.value = value

class Date(Symbol):
    def __init__(self, key:str, value:str|None):
        super().__init__(key, str)
        self.update(value)

    def __str__(self) -> str:
        if not self.value:
            return str(self.value)
        return self.value.strftime('%Y-%m-%d')

    def update(self, value:str|None) -> None:
        self.matchType(value)
        if value:
            try:
                self.value = date.fromisoformat(value)
            except ValueError:
                raise exceptions.RuntimeError('Fecha de formato no valido. Usar YYYY-MM-DD')
        else:
            self.value = value

class DateTime(Symbol):
    def __init__(self, key:str, value:str|None):
        super().__init__(key, str)
        self.update(value)

    def __str__(self) -> str:
        if not self.value:
            return str(self.value)
        return self.value.strftime('%Y-%m-%d %H:%M:%S')

    def update(self, value:str|None) -> None:
        self.matchType(value)
        if value:
            try:
                self.value = datetime.fromisoformat(value)
            except ValueError:
                raise exceptions.RuntimeError('Fecha-hora de formato no valido. Usar YYYY-MM-DD HH:mm:ss')
        else:
            self.value = value
