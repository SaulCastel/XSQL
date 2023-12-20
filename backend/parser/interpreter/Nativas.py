from datetime import datetime


def isString(cadena) -> bool:
    return isinstance(cadena, (str))

def isNumber(numero) -> bool:
    return isinstance(numero, (int)) 

class Concatenar:
    def __init__(self,cadena1,cadena2) -> None:
        self.cadena1=cadena1
        self.cadena2=cadena2
    def interpret(self):
        cadena1= self.cadena1.interpret()
        cadena2=self.cadena2.interpret()
        
        if isString(cadena1) and isString(cadena2):
            return cadena1 + cadena2
        else :
            print("los argumentos deben ser str")

class Substaer :
    def __init__(self,cadena,inicio, longitud) -> None:
        self.cadena = cadena
        self.inicio=inicio
        self.longitud =longitud
    
    def interpret(self):
        cadena =self.cadena.interpret()
        inicio =self.inicio.interpret()
        longitud =self.longitud.interpret()

        if isString(cadena) and isNumber(inicio) and isNumber(longitud):
            return cadena[inicio-1:inicio-1+longitud]
        else:
            print ("los parametros deben ser (str,int,int)")

class hoy :
    def __init__(self,) -> None:
        pass
    
    def interpret(self):
        from datetime import datetime

        fecha_hora_actual = datetime.now()
        
        formato_personalizado = "%d-%m-%Y %H:%M"
        fecha_hora_formateada = fecha_hora_actual.strftime(formato_personalizado)

        return fecha_hora_formateada

class contar:
    def __init__(self,nameTabla,expresion,base) -> None:
        self.nameTabla =nameTabla
        self.expresion=expresion
        self.base=base
    
    def interpret(self):
        expresion=self.expresion.interpret()
        print(self.expresion.left)
        print(expresion)
