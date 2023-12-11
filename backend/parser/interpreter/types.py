class INT:
    def __init__(self, val):
        self.val = int(val)

class DECIMAL:
    def __init__(self, val):
        self.val = float(val)

class BIT:
    def __init__(self, val):
        self.val = int(val) 

class NCHAR:
    def __init__(self, val, size):
        self.val = val
        self.size = size

class NVARCHAR:
    def __init__(self, val, size):
        self.val = val
        self.size = size
