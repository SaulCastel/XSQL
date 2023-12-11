class RuntimeError(Exception):
    def __init__(self, message:str, position:tuple) -> None:
        '''Raised on runtime exception when interpreting xsql'''
        super().__init__(f'Error al ejecutar en {position}: {message}')
