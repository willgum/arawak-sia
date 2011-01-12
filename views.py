# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                 

def indice(request):
    plantilla = get_template('index.html')
    variables = Context({
        'user': request.user, 
        'titulo_pestana': '.:SIA - Sistema de Información Académica:.',
        'titulo_pagina': '.:SIA:.',
        'titulo_descriptivo': 'Sistema de Información Académica',
        'titulo_seccion_azul': 'Bienvenido ',
        'titulo_seccion_verde': 'Instituto Syspro',
        'mes': 'Ene',
        'dia': '11',
        'path': settings.MEDIA_URL,
    })
    salida = plantilla.render(variables)
    return HttpResponse(salida)

def login(request):
    username = request.POST['usuario']
    password = request.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)        
        return HttpResponseRedirect(request.POST['next'])
    else:        
        return HttpResponseRedirect("/")

def logout(request):
    auth.logout(request)    # Redirect to a success page.
    return HttpResponseRedirect("/")