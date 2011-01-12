from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    # definicion de urls para la aplicacion academico     
    (r'^$', indice),    
)