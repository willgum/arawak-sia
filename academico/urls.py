from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    # contrasena y actualizar contrasena
    (r'^programas/$', programas),  
)