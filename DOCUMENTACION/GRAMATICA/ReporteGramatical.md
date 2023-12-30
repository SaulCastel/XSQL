# GRAMATICA 

## Expresiones regulares:

    number = [0-9]+
    
    decimal = {number}[.]{number}
    
    doubleQuoteString = [^"]*
    
    singleQuoteString = [^']*
    
    string = {doubleQuoteString}|{singleQuoteString}
    
    identifier = [a-z_][a-z0-9_]*

## Precedencia Utilizada:

### 
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', '!'),
    ('left', 'EQUALS', 'NOT_EQUALS', '<', '>', 'LESS_EQUALS', 'GREATER_EQUALS'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),

## Simbolos terminales:
    1.  WHERE
    2.  SELECT
    3.  FROM
    4.  DECLARE
    5.  CREATE
    6.  DATA
    7.  BASE
    8.  TABLE
    9.  PROCEDURE
    10. FUNCTION
    11. RETURN
    12. AS
    13. BEGIN
    14. END
    15. ALTER
    16. ADD
    17. DROP
    18. INT
    19. DECIMAL
    20. DATE
    21. DATETIME
    22. NCHAR
    23. NVARCHAR
    24. USAR
    25. INSERT
    26. INTO
    27. VALUES
    28. PRIMARY
    29. REFERENCE
    30. KEY
    31. NOT
    32. NULL
    33. CONCATENAR
    34. SUBSTRAER
    35. HOY
    36. CONTAR
    37. SET
    38. TRUNCATE
    39. DELETE
    40. UPDATE
    41. WHILE
    42. IF
    43. CASE
    44. WHEN
    45. THEN
    46. ELSE
    47. LESS_EQUALS 
    48. GREATER_EQUALS 
    49. EQUALS 
    50. NOT_EQUALS 
    51. AND 
    52. OR
    53. DECIMAL_LITERAL 
    54. INT_LITERAL 
    55. STRING_LITERAL 
    56. IDENTIFIER

## Simbolos no terminales:
     
    1.  script
    2.  stmts
    3.  stmt
    4.  table_structure
    5.  column_declaration
    6.  nullity
    7.  key_type
    8.  ListNewAssignment
    9.  identifiers
    10. exprs
    11. selection_list
    12. alias
    13. where
    14. condition
    15. condition_expr
    16. expr
    17. literal
    18. symbol
    19. varCall
    20. native
    21. type
    22. empty
    23. Fin_If
    24. List_When
    25. options_When
    26. options
    27. finCase    

## Explicacion de Simbolos Terminales:

1. WHERE: Cláusula utilizada en declaraciones condicionales para filtrar registros en base a ciertas condiciones.

2. SELECT: Cláusula utilizada para seleccionar datos de una tabla o expresiones en el lenguaje XSQL.

3. FROM: Cláusula utilizada para especificar la tabla de la cual seleccionar datos en una declaración SELECT.

4. DECLARE: Palabra clave utilizada para declarar variables en el lenguaje.

5. CREATE: Palabra clave utilizada para crear estructuras de datos, como tablas o bases de datos.

6. DATA: Palabra clave utilizada en la creación de bases de datos.

7. BASE: Palabra clave utilizada en la creación de bases de datos.

8. TABLE: Palabra clave utilizada en la creación de tablas.

9. PROCEDURE: Palabra clave utilizada para definir procedimientos almacenados.

10. FUNCTION: Palabra clave utilizada para definir funciones.

11. RETURN: Palabra clave utilizada para devolver un valor desde una función.

12. AS: Palabra clave utilizada en la declaración de variables para especificar su tipo.

13. BEGIN: Marca el inicio de un bloque de código.

14. END: Marca el final de un bloque de código.

15. ALTER: Palabra clave utilizada para modificar la estructura de una tabla.

16. ADD: Palabra clave utilizada con ALTER para agregar elementos a una tabla.

17. DROP: Palabra clave utilizada con ALTER para eliminar elementos de una tabla.

18. INT: Palabra clave que representa el tipo de datos entero.

19. DECIMAL: Palabra clave que representa el tipo de datos decimal.

20. DATE: Palabra clave que representa el tipo de datos fecha.

21. DATETIME: Palabra clave que representa el tipo de datos fecha y hora.

22. NCHAR: Palabra clave que representa el tipo de datos de cadena de longitud fija.

23. NVARCHAR: Palabra clave que representa el tipo de datos de cadena de longitud variable.

24. USAR: Palabra clave utilizada para cambiar la base de datos en uso.

25. INSERT: Palabra clave utilizada para insertar datos en una tabla.

26. INTO: Palabra clave utilizada en la cláusula INSERT para especificar la tabla de destino.

27. VALUES: Palabra clave utilizada en la cláusula INSERT para especificar los valores que se insertarán.

28. PRIMARY: Palabra clave utilizada en la definición de claves primarias.

29. REFERENCE: Palabra clave utilizada en la definición de claves foráneas.

30. KEY: Palabra clave utilizada en la definición de claves.

31. NOT: Palabra clave utilizada para negar una condición.

32. NULL: Palabra clave que representa la ausencia de valor.

33. CONCATENAR: Palabra clave que representa la función de concatenación de cadenas.

34. SUBSTRAER: Palabra clave que representa la función de substracción de cadenas.

35. HOY: Palabra clave que representa la función que devuelve la fecha actual.

36. CONTAR: Palabra clave que representa la función de contar elementos.

37. SET: Palabra clave utilizada para asignar valores a variables.

38. TRUNCATE: Palabra clave utilizada para vaciar una tabla.

39. DELETE: Palabra clave utilizada para eliminar registros de una tabla.

40. UPDATE: Palabra clave utilizada para actualizar registros en una tabla.

41. WHILE: Palabra clave que inicia un bucle WHILE.


42. IF: Palabra clave que inicia una estructura condicional IF.

43. CASE: Palabra clave que inicia una estructura condicional CASE.

44. WHEN: Palabra clave utilizada en una estructura condicional CASE para especificar condiciones.

45. THEN: Palabra clave utilizada en estructuras condicionales para indicar las acciones a realizar si se cumple la condición.

46. ELSE: Palabra clave utilizada en estructuras condicionales para indicar las acciones a realizar si no se cumple ninguna condición previa.

47. LESS_EQUALS: Símbolo utilizado para representar la comparación "menor o igual".

48. GREATER_EQUALS: Símbolo utilizado para representar la comparación "mayor o igual".

49. EQUALS: Símbolo utilizado para representar la comparación de igualdad.

50. NOT_EQUALS: Símbolo utilizado para representar la comparación de desigualdad.

51. AND: Símbolo utilizado para representar la operación lógica "y".

52. OR: Símbolo utilizado para representar la operación lógica "o".

53. DECIMAL_LITERAL: Representa un literal decimal en el código.

54. INT_LITERAL: Representa un literal entero en el código.

55. STRING_LITERAL: Representa un literal de cadena en el código.

56. IDENTIFIER: Representa un identificador (nombre de variable, tabla, etc.) en el código.

## Explicacion de Simbolos No Terminales:

1. script: Representa el script principal, que es la unidad básica de ejecución. Puede contener un conjunto de declaraciones (stmts).

2. stmts: Es una lista de declaraciones (stmt). En el contexto del script, es la secuencia de declaraciones que forman el cuerpo principal del código.

3. stmt: Representa una declaración en el lenguaje. Puede ser una variedad de declaraciones, como USAR, CREATE, INSERT, DELETE, UPDATE, SELECT, DECLARE, SET, WHILE, IF, CASE, entre otras.

4. table_structure: Representa la estructura de una tabla en una declaración CREATE TABLE. Incluye las declaraciones de las columnas y sus atributos.

5. column_declaration: Describe la declaración de una columna en una tabla. Incluye el nombre de la columna, su tipo de datos, si puede contener valores nulos (nullity), y si es clave primaria (key_type).

6. nullity: Indica si una columna puede contener valores nulos (NULL) o no (NOT NULL).

7. key_type: Indica el tipo de clave que puede tener una columna, por ejemplo, clave primaria (PRIMARY KEY).

8. ListNewAssignment: Lista de asignaciones en una declaración. Es utilizada en contextos como la asignación de valores a variables.

9. identifiers: Lista de identificadores. Se utiliza en contextos como la definición de columnas o la cláusula INSERT INTO para especificar las columnas afectadas.

10. exprs: Lista de expresiones. Se utiliza en contextos como la cláusula VALUES de una declaración INSERT.

11. selection_list: Lista de expresiones seleccionadas en una declaración SELECT.

12. alias: Representa un alias para una expresión o columna seleccionada en una declaración SELECT.

13. where: Representa la cláusula WHERE en una declaración condicional. Define la condición que se debe cumplir para ejecutar ciertas acciones.

14. condition: Representa una condición booleana utilizada en declaraciones condicionales como IF o CASE.

15. condition_expr: Representa una expresión condicional utilizada en declaraciones condicionales.

16. expr: Representa una expresión aritmética o lógica en diversas situaciones.

17. literal: Representa un valor literal, como un número entero, decimal o cadena.

18. symbol: Representa un símbolo o identificador en una expresión.

19. varCall: Representa la llamada a una variable.

20. native: Representa funciones nativas incorporadas en el lenguaje.

21. type: Representa el tipo de datos, como entero, decimal, fecha, etc.

22. empty: Representa una producción nula. Indica que ciertas producciones pueden ser opcionales.

23. Fin_If: Representa la cláusula ELSE en una estructura condicional IF.

24. List_When: Lista de condiciones WHEN en una estructura condicional CASE.

25. options_When: Representa las opciones en una cláusula WHEN de una estructura condicional CASE.

26. options: Representa las opciones en una estructura condicional CASE.

27. finCase: Representa la cláusula ELSE en una estructura condicional CASE


