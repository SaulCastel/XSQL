from parser.interpreter.exceptions import RuntimeError
from parser.interpreter.context import Context
from parser import xsql
from fastapi import FastAPI, Body
from typing import Annotated
import uvicorn

app = FastAPI()

@app.post('/interpret')
def interpret(body: Annotated[dict, Body()]):
    stmts = xsql.parser.parse(body['input'])
    parserState = {
        'database': '',
        'output': [],
        'result': [],
    }
    globalContext = Context()
    try:
        for stmt in stmts:
            stmt.interpret(globalContext, parserState)
    except RuntimeError as error:
        parserState['output'].append(str(error))
    return {
        'output': parserState['output'],
        'result': parserState['result'],
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
