from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    (r'^$', indice),
    (r'^programas/$', programas),
    
    (r'^competencias/$', competencias), 
    (r'^competencias/(?P<competencia_id>\d+)/$', competenciasDetalle),
    
    (r'^horarios/$', horarios),
    (r'^horarios/(?P<competencia_id>\d+)/$', competenciasDetalle), 
    
    (r'^notas/$', notas),
    (r'^notas/(?P<competencia_id>\d+)/$', competenciasDetalle),
    (r'^notas/ingresar/(?P<curso_id>\d+)/$', ingresarNota),
    
    (r'^notas/ingresar/\d+/guardarNota/$', guardarNota),
    (r'^notas/ingresar/\d+/guardarFallas/$', guardarFallas),
)