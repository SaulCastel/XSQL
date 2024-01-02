class RuntimeError(Exception):
    def __init__(self, message:str, position:tuple|None=None) -> None:
        '''Raised on runtime exception when interpreting xsql'''
        if position:
            super().__init__(f'Error al ejecutar en {position}: {message}')
        else:
            super().__init__(f'Error al ejecutar: {message}')

class ParsingError(Exception):
    def __init__(self, message:str, lineno) -> None:
        super().__init__(f'Error de parseo en fila {lineno}: {message}')

class Return(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value
