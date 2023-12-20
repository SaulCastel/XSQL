from parser.xsql import parser
from parser.interpreter.exceptions import RuntimeError

if __name__ == '__main__':
   # while 1:
        try:
           # text = input('entry > ')
            text =  '''
                CREATE DATA BASE tbbanco;  
                USAR tbbanco; 
                CREATE TABLE tbidentificaciontipo (
                ididentificaciontipo int PRIMARY KEY,
                identificaciontipo nchar(50) not null);
              
              '''
                   
            tree = parser.parse(text)
            for stmt in tree:
                stmt.interpret()
        except RuntimeError as error:
            print(error)  
