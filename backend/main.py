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
        'block': 0,
        'symbols': [],
        'ast':[],
    }
    try:
        xsql.lexer.errors = []
        xsql.parser.errors = []
        xsql.lexer.input(body['input'])
        stmts = xsql.parser.parse()
        if len(xsql.lexer.errors) > 0 or len(xsql.parser.errors) > 0:
            raise exceptions.ParsingError('Errores en parseo. Cancelando ejecución.', 0)
        try:
            globalContext = Context(prev=None,name='Global')
            for stmt in stmts:
                stmt.interpret(globalContext, parserState)
            parserState['symbols'].extend(globalContext.dump())
        except exceptions.RuntimeError as error:
            parserState['output'].append(str(error))

        dot = 'graph AST {\n'
        dot += 'ordering = out\n'
        #dot += 'node [shape=plaintext]\n'
        dot += stmts[0].GenerarAST()
        dot += '"MasStmt0"[label = "stmts"]\n'
        dot += f'"MasStmt0" -- "stmt{stmts[0].contador}"\n'
        for a in range(1, len(stmts)):
            dot += f'"MasStmt{a-1}" -- "stmt{stmts[a].contador}"\n'
            dot += stmts[a].GenerarAST()
            dot += f'"MasStmt{a}"[label = "stmts"]\n'
            dot += f'"MasStmt{a}" -- "MasStmt{a-1}"\n'
        dot += '}'
        with open('ast.dot', 'w') as file:
            file.write(dot)
        parserState['ast'].append(str(dot))
    except exceptions.ParsingError as error:
        parserState['output'].append(str(error))
    return {
        'output': parserState['output'],
        'result': parserState['result'],
        'errors': [*xsql.lexer.errors, *xsql.parser.errors],
        'symbols': parserState['symbols'],
        'ast':parserState['ast'],
    }



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
