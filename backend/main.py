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
        stmts = xsql.parser.parse(body['input'])
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

@app.post('/GenerarAST')
def GenerarAST(body: Annotated[dict, Body()]):
    MAnejoAST = {
        'output': [],
        'result': [],
    }
    try:
        stmts = xsql.parser.parse(body['input'])
        try:
            dot = 'graph AST {\n'
            dot += 'ordering = out\n'
            dot += stmts[0].GenerarAST()
            dot += '"stmt0"[label = "stmt"]\n'
            dot += f'"stmt0" -- "instruc{stmts[0].contador}"\n'

            dot += '}'
            print (dot)
            MAnejoAST['result'].append(str(dot))
        except exceptions.RuntimeError as error:
            MAnejoAST['output'].append(str(error))
    except exceptions.ParsingError as error:
        MAnejoAST['output'].append(str(error))
    return {
        'output': MAnejoAST['output'],
        'result': MAnejoAST['result'],
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
