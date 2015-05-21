#Guía para agregar nuevas características al proyecto cuando la aplicación ya está en producción.

# Cómo agregar nuevas características cuando la aplicación está en producción #

## Crear nuevos modelos o agregar o quitar atributos a modelos ##

  * En primer lugar, deberá hacerse una copia de seguridad de la información. Hay dos formas posibles: Ingresar al panel de control y desde el phpmyadmin generar la copia de respaldo. La segunda es generando la información a archivo `*`.json, mediante el comando ` python manage.py dumpdata nombremodelo > nombrearchivo.json `.

  * Luego de hacer la copia de seguridad, deberá realizarse las modificaciones respectivas a la base de datos, como los caso de alter table o create table, según el caso.

  * Aunque no es necesario, puede sincronizar la base de datos por medio del comando python manage.py syncdb.


## Actualizar los archivos de aplicación ##

Para actualizar los archivos de aplicación que no sean los de configuración, deberá ubicarse en el servidor. Dirigirse a la carpeta webapps/_nombreproyecto_/lib/python2.6. Una vez allí actualice los archivos correspondientes.

Luego deberá reiniciar la instancia apache de la aplicación. Ésta se encuentra en webapps/_nombreproyecto_/apache2/bin. Desde la consola de comandos ejecute ` ./stop ` y luego ` ./start `. Una vez reiniciada la instancia de apache, la aplicación tomará los cambios respectivos.