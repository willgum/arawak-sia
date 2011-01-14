from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from views import *                         # maneja la vista para el index de la aplicacion
from django.views.static import *           # se incorporo para poder acceder a archivos estaticos
from django.conf import settings            # se incopora para poder acceder a los valores creados en el settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # definicion de urls para la aplicacion academico     
    (r'^$', indice),
    
    # login/logout
    (r'^login/$', login),
    (r'^logout/$', logout),
    
    # definicion de urls para la aplicacion academico     
    (r'^academico/', include('academico.urls')),
    
    # administrador de la aplicacion
    (r'^admin/', include(admin.site.urls)),
    
    # esta linea es necesaria para poder acceder a documentos archivos estaticos como css e imagenes    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)