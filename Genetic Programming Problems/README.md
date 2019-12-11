### Tarea 3: Programación Genética

#### Modificación para soporte de variables
Dentro del archivo *arboles.py*, en el método *eval* de la clase *Node*, se agregó un argumento de tipo 
diccionario que recibe las variables con los valores que se le asignarán para evaluar la función. Los 
terminales que no corresponden a números, se les debe otorgar como llave y valor el mismo número. 
Asimismo, se modificó la función *eval* de la clase *TerminalNode*.

Para el ejercicio en el que se debe encontrar número, y sus variantes, simplemente se agregó el 
diccionario con el método mencionado en el párrafo anterior: dado que no hay variables sólo se
añadieron números.

### Implementación del nodo División
#### División por cero
Para evitar dividir por cero, en primer lugar se capturó la excepción *ZeroDivisionError* al correr 
el algoritmo de programación genética, dentro del archivo *symbolic_regression_with_div.py*. A su vez,
se debió capturar la misma excepción al evaluar la expresión contenida en el árbol en cada punto del
rango [-100, 100], dentro del método *fitness_4* del mismo archivo. Si la expresión evaluada contiene
una división por cero, entonces inmediatamente se castiga a la función de fitness del árbol asignándole 
el máximo valor de tipo int disponible (*sys.maxsize*), ya que se está minimizando. Este número se eligió 
por simplicidad, pero bastaba un valor lo suficientemente grande e inalcanzable sólo para la función 
de fitness. Por otro lado, el castigo a la función de fitness pudo haber sido menos severo, pero este
tipo de árboles requerían considerarse inválidos.