from parser.xsql import parser
from parser.interpreter.exceptions import RuntimeError

if __name__ == '__main__':
    while 1:
        try:
            text = input('entry > ')
            tree = parser.parse(text)
            for stmt in tree:
                print(stmt.interpret())
        except RuntimeError as error:
            print(error)  
