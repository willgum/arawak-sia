from django.conf.urls.defaults import *
from financiero.views import *

urlpatterns = patterns('',
    #urls para estudiantes
    (r'^$', indice),
    (r'^estudiante/$', indice),
    (r'^estudiante/pazysalvo/$', pazySalvo),
    (r'^estudiante/pazysalvo/plazo/$', pazySalvo),
    (r'^estudiante/pazysalvo/plazo/(?P<letra_id>\d+)/$', pazySalvoParcial),
    (r'^estudiante/pazysalvo/(?P<inscripcionPrograma_id>\d+)/$', pazySalvoTotal)
)