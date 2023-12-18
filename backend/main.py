from parser.interpreter.exceptions import RuntimeError
from parser import xsql
from fastapi import FastAPI, Body
from typing import Annotated

app = FastAPI()

@app.post('/interpret')
def interpret(body: Annotated[dict, Body()]):
    stmts = xsql.parser.parse(body['input'])
    parserState = {
        'database': '',
        'output': [],
        'result': {}
    }
    try:
        for stmt in stmts:
            stmt.interpret()
    except RuntimeError as error:
        parserState['output'].append(str(error))
    return {
        'output': parserState['output'],
        'result': parserState['result'],
    }
