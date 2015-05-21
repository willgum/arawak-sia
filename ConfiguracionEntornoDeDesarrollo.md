# Software #

  * [Django Stack 1.2.3-0](http://bitnami.org/stack/djangostack)
  * [Eclipse Classic 3.6.1](http://www.eclipse.org/downloads/)
    * [Pydev](http://pydev.org/): http://pydev.org/updates
    * [Mercurial for Eclipse](http://javaforge.com/project/HGE): http://cbes.javaforge.com/update
    * [SQL Explorer](http://www.sqlexplorer.org/) http://eclipsesql.sourceforge.net/

## Configuración MAC ##

  * Instalar MySQL
  * Agregar `alias mysql=/usr/local/mysql/bin/mysql` y `alias mysqladmin=/usr/local/mysql/bin/mysqladmin` al archivo `~/.bash_profile`
    * Ejecutar `> sudo mysqld_safe` para iniciar el servidor de bases de datos
  * Python 2.7.1 http://www.python.org/download/
  * Instalar setuptools http://pypi.python.org/pypi/setuptools, se descarga el .egg y se ejecuta `> sh setuptools-0.6c9-py2.7.egg`
  * Ejecutar `> easy_install mysql-python`
  * Ejecutar `> easy_install image`
  * Ejecutar `> easy_install django`
  * Agregar `export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/` al archivo `~/.bash_profile`
  * Ejecutar `> source ~/.bash_profile`
  * Ejecutar `> python`
  * Ejecutar `>>> import Image`, `>>> import MySQLdb`, `>>> import django`, si no hay error los módulos estan instaldos correctamente


# Enlaces de interés #

  * [Guia de Mercurial](http://hgbook.red-bean.com/)
  * [Video de configuración Eclipse Django](http://vimeo.com/5027645)
  * [Tutorial Django](http://docs.djangoproject.com/en/1.2/intro/tutorial01/)
  * [Referencia Campos Django](http://docs.djangoproject.com/en/1.2/ref/models/fields/)
  * [Documentación Django](http://docs.djangoproject.com/en/1.2/)