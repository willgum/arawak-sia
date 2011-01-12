# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib.auth.decorators import login_required       # me permite usar eö @login_requerid

@login_required
def indice(request):
    plantilla = get_template('academico/index.html')
    variables = Context({
        'user': request.user, 
        'titulo_pestana': '.:SIA - Sistema de Información Académica:.',
        'titulo_pagina': '.:SIA:.',
        'titulo_descriptivo': 'Sistema de Información Académica',
        'titulo_seccion_azul': '.:Instituto ',
        'titulo_seccion_verde': 'Syspro:.',
        'path': settings.MEDIA_URL,
    })
    salida = plantilla.render(variables)
    return HttpResponse(salida)