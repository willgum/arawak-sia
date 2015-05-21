# Hosting #

  * http://docs.webfaction.com/software/django/index.html


# Configurando Django en webfaction #

A partir de la guía de introducción a Django publicada en la página de documentación de webfaction:

http://docs.webfaction.com/software/django/getting-started.html#getting-started-with-django.

  * En primer lugar se crea una aplicación django con nombre sia, desde el panel de control. Esta operación instalará la aplicación django dentro de /home/arawak/webapps/ con nombre sia. La aplicación contiene unas subcarpetas, de las cuales se tendrán en cuenta las siguientes:
  1. **Apache2**. Contiene la subcarpeta bin con la aplicación ./restart, que debe ejecutarse cada vez que se sube un cambio en los archivos `*`.py.
  1. **lib**. Contiene la subcarpeta python2.6. Dentro de la carpeta python quedará instaladas las aplicaciones que sean construidas para nuestro projecto Django (academico, continuada, financiero, egresados, etc); a su vez contiene una aplicación de nombre django.
  1. **myproject**. Contiene los archivos de configuración de nuestro proyecto Django (manage.py, settings.py, urls.py, etc). Dentro de myproject se copia la carpeta media que contiene las subcarpetas css, imagenes, images, js. También se copia la carpeta template que contiene las plantillas del proyecto.

  * Se crea un link simbólico (Symbolic link to static-only app) que apunta a la carpeta de nombre media ubicada en la carpeta myproject de la aplicación sia /home/arawak/webapps/sia/myproject.

  * Se crea otro link simbólico (Symbolic link to static-only app) que apunta a la carpeta de la aplicación django /home/arawak/webapps/sia/lib/python2.6/django/contrib/admin/media.

  * Se crea la base de datos, en este caso mysql, con nombre arawak\_sia.

  * El siguiente paso es configurar en el panel de control de WebFaction para que enlace con la aplicación django, a la carpeta media del projecto y a la carpeta media del admin de Django:
  1. En primer lugar debe darse clic en Domains / websites - Websites.
  1. Se Crea un nuevo sitio, se selecciona el subdominio al que está relacionado y se agrega las tres aplicaciones creadas: APP: 'sia', URL: '/'. APP: 'media\_admin', URL: '/admin/media'. APP: 'media', URL: '/media'.

  * Ahora se edita el archivo /home/arawak/webapps/sia/myproject/settings.py:
  1. Se agrega una tupla a _ADMINS_ que contenga el nombre de usuario y correo electrónico del administrador.
  1. En _DATABASES_ se establece el _ENGINE_ a _django.db.backends.mysql_. También se establece el nombre de la base de datos _NAME_, el nombre de usuario _USER_ y la contraseña _PASSWORD_ para la base de datos creada anteriormente.
  1. Se establece el _MEDIA\_ROOT_ a _"/home/arawak/webapps/media/"_.
  1. Se establece el _MEDIA\_URL_ a _"http://sia.arawak.webfactional.com/media/"_.
  1. Se establece el _ADMIN\_MEDIA\_PREFIX_ a _"http://sia.arawak.webfactional.com/admin/media/"_.
  1. Se agrega la siguiente línea a _TEMPLATE\_DIRS_: _"/home/arawak/webapps/sia/myproject/template"_.
  1. En _INSTALLED\_APPS_ se agrega _"django.contrib.admin"_, _"academico"_, _"contiuada"_, _"financiero"_, _"egresados"_.

  * Se edita el archivo urls.py que se encuentra en _/home/arawak/webapps/sia/myproject/urls.py_ y se descomentan las líneas _from django.contrib import admin, admin.autodiscover()_, _(r'`^`admin/doc/', include('django.contrib.admindocs.urls'))_, y _(r'`^`admin/', include(admin.site.urls)),_.

  * Finalmente debe sincronizarse la base de datos y reiniciar la instancia apache, desde una consola SSH:
  1. Ubicarse en la carpeta del proyecto _/home/arawak/webapps/sia/myproject/_.
  1. Ejecutar _python2.6 manage.py syncdb_. La base de datos será actualizada.
  1. Ubicarse ahora en el directorio bin de apache _/home/arawak/webapps/sia/apache2/bin_ y ejecutar ./restart.

  * Ahora podrá visualizarse el sitio desde http://sia.arawak.webfactional.com/.

Para generar los reportes en formato pdf, deberá instalar Geraldo reports y reportlab con la siguiente instrucción: _easy\_install reportlab geraldo_. Además, en el archivo _settings.py_ agregar en _INSTALLED\_APPS_ el aplicativo _geraldo_.

Si se va a instalar Geraldo en un equipo con sistema operativo windows, instale en primer lugar reportlab desde el archivo _.exe_ correspondiente. Seguido descargue el comprimido Geraldo, descomprímalo y abra la carpeta correspondiente. Luego ejecute el instalador con _python setup.py install_.