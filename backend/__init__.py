from flask import Flask, request
from parser import xsql

app = Flask(__name__)

@app.post('/interpret')
def interpret():
    body = request.get_json()
    stmts = xsql.parser.parse(body['input'])
    parserState = {}
    for stmt in stmts:
        parserState = stmt.interpret(parserState)
    return {
        'output': parserState['output'],
        'result': parserState['result'],
    }
