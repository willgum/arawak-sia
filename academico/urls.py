from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    # ver programas a los que un docente o profesor se encuetra vinculado
    (r'^programas/$', programas),
    (r'^programas/(?P<programa_id>\d+)/$', programasDetalle), 
    
    (r'^competencias/$', competencias), 
    (r'^competencias/(?P<competencia_id>\d+)/$', competenciasDetalle),
)