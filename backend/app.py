from parser.xsql import parser

if __name__ == '__main__':
    while 1:
        text = input('entry > ')
        tree = parser.parse(text)
        for stmt in tree:
            print(stmt.interpret())
