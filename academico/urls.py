from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    (r'^$', indice),
    
    (r'^programas/$', programas),
    (r'^programas/(?P<programa_id>\d+)/$', programasDetalle), 
    
    (r'^competencias/$', competencias), 
    (r'^competencias/(?P<competencia_id>\d+)/$', competenciasDetalle),
    
    (r'^horarios/$', horarios),
    (r'^horarios/(?P<competencia_id>\d+)/$', competenciasDetalle), 
)