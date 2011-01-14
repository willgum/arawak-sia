# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                 
from django.contrib.auth.models import Group

def indice(request):
    plantilla = "index.html",
    variables = Context({
        'user': request.user, 
        'titulo_pestana': '.:SIA - Sistema de Información Académica:.',
        'titulo_pagina': '.:SIA:.',
        'titulo_descriptivo': 'Sistema de Información Académica',
        'titulo_seccion_azul': 'Bienvenido ',
        'titulo_seccion_verde': 'Instituto Syspro',
        'fecha': datetime.datetime.today(),
        'path': settings.MEDIA_URL,
    })
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

def login(request):
    username = request.POST['usuario']
    password = request.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)   
        return HttpResponseRedirect("/")
    else:        
        return HttpResponseRedirect("/")

def logout(request):
    auth.logout(request)    
    return HttpResponseRedirect("/")