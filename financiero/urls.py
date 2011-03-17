from django.conf.urls.defaults import *
from financiero.views import *

urlpatterns = patterns('',
    #urls para estudiantes
    (r'^$', indice),
    (r'^estudiante/$', indice),
    (r'^estudiante/pazysalvo/', pazySalvo),
)