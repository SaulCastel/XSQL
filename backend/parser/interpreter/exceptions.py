class RuntimeError(Exception):
    def __init__(self, message:str, position:tuple|None=None) -> None:
        '''Raised on runtime exception when interpreting xsql'''
        if position:
            super().__init__(f'Error al ejecutar en {position}: {message}')
        else:
            super().__init__(f'Error al ejecutar: {message}')
