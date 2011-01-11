# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings


def indice(request):
    plantilla = get_template('index.html')
    variables = Context({
        'user': request.user, 
        'titulo_ventana': '.:SIA:.',
        'titulo_descrptivo': 'Sistema de Información Académica',
        'cuerpo': 'Instituto Syspro',
        'path': settings.MEDIA_URL,
    })
    salida = plantilla.render(variables)
    return HttpResponse(salida)