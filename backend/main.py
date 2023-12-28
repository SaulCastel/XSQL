from parser.interpreter import exceptions
from parser.interpreter.context import Context
from parser import xsql
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import uvicorn

app = FastAPI()

# # Configuración CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto a los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/interpret')
def interpret(body: Annotated[dict, Body()]):
    parserState = {
        'database': '',
        'output': [],
        'result': [],
    }
    try:
        xsql.lexer.input(body['input'])
        stmts = xsql.parser.parse()
        try:
            globalContext = Context()
            for stmt in stmts:
                stmt.interpret(globalContext, parserState)
        except exceptions.RuntimeError as error:
            parserState['output'].append(str(error))
    except exceptions.ParsingError as error:
        parserState['output'].append(str(error))
    return {
        'output': parserState['output'],
        'result': parserState['result'],
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
