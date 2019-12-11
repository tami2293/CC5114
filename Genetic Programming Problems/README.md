### Tarea 3: Programación Genética

#### Modificación para soporte de variables
Dentro del archivo *arboles.py*, en el método *eval* de la clase *Node*, se agregó un argumento de tipo 
diccionario que recibe las variables con los valores que se le asignarán para evaluar la función. Los 
terminales que no corresponden a números, se les debe otorgar como llave y valor el mismo número. 
Asimismo, se modificó la función *eval* de la clase *TerminalNode*.

Para el ejercicio en el que se debe encontrar número, y sus variantes, simplemente se agregó el 
diccionario con el método mencionado en el párrafo anterior: dado que no hay variables sólo se
añadieron números.