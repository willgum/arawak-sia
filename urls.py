from django.conf.urls.defaults import *
from academico.views import *
from django.views.static import *           # se incorporo para poder acceder a archivos estaticos
from django.conf import settings            # se incopora para poder acceder a los valores creados en el settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', indice),
    (r'^admin/', include(admin.site.urls)),
    
    # esta linea es necesaria para poder acceder a documentos archivos estaticos como css e imagenes    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
