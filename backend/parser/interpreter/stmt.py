class Select:
    def __init__(self, exprs:list) -> None:
        self.exprs = exprs

    def interpret(self):
        for expr in self.exprs:
            print(expr[0].interpret(), expr[1], sep=' AS ')

class SelectFrom:
    def __init__(self, selection:list, table:str, condition):
        self.selection = selection
        self.table = table
        self.condition = condition
