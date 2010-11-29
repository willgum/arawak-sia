from django.conf.urls.defaults import *
from academico.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', main_page),
    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^estudiante/(\w+)/$', estudiante_pagina),
    # (r'^login/$', 'django.contrib.auth.views.login'),
)
