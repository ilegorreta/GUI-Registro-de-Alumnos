# Registro de Alumnos GUI

Desarrollar una interfaz gráfica de un registro de alumnos, la cual al iniciar
deberá de pedir el usuario del administrador y su contraseña para poder
acceder. Al ingresar se tendrá lo siguiente:

* Una tabla con la lista de los alumnos registrados con sus respectivos datos
ordenados por Fecha y Hora de registro.
* Una gráfica con las edades de los alumnos. X=>Edad , Y=>Numero de
alumnos.
* Una tabla con todas las escolaridades registradas y su numero de alumnos
de cada una.
* Un botón para eliminar todos los registros de alumnos. Al hacer click en
dicho botón se deberá de pedir la contraseña del administrador para
confirmar el borrado de datos.
* Un botón para agregar un nuevo alumno, el cual deberá abrir una ventana
con un formulario para agregar los siguientes datos del alumno (Se deberá
de validar cada dato):
    * Nombre
    * Edad
    * Escolaridad
    * Fecha
    * Hora
* Un botón de guardar, el cual creará una trama en formato JSON (usted la
deberá de estructurar) con el contenido de todos los alumnos registrados y
dicha trama se deberá de guardar en un archivo de texto.
* Un botón de cargar, el cual cargará los registros de los alumnos que hayan
sido guardados previamente en un archivo de texto con alguna trama JSON
previamente guardada.

## Notas Importantes

* Usuario de admin: **root**
* Password de admin: **toor**
* Script desarrollado en **Python 3.8.3**, **Ubuntu 18.04** y **ambiente virtual conda**
* En el script vienen especificadas las librerías utilizadas, díganme si necesitan que les comparta mi ambiente virtual con dichas dependencias instaladas
* En el repo hay 2 archivos JSON donde realicé pruebas. Ustedes pueden generar nuevos archivos utilizando el propio programa.