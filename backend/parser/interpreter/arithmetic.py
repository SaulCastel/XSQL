from .exceptions import RuntimeError
from . import types
from datetime import date, datetime

def sum(left, right, position):
    if isinstance(left, (types.INT, types.DECIMAL)):
        if isinstance(right, (types.INT, types.DECIMAL, types.BIT)):
            return left.val + right.val
        elif isinstance(right, (types.NCHAR, types.NVARCHAR)):
            return str(left.val) + right.val
    elif isinstance(left, (types.NCHAR, types.NVARCHAR)):
        if not isinstance(right, (date, datetime)):
            return left.val + str(right.val)
    leftType = type(left).__name__
    rightType = type(right).__name__
    raise RuntimeError(f'No se puede sumar {leftType} con {rightType}', position)
