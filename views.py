# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                   # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                    # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   

def indice(request):
    plantilla = "index.html",
    variables = Context({
        'user': request.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,
    })
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

def login(request):
    username = request.POST['usuario']
    password = request.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    plantilla = "index.html",    
    if user is None:
        variables = Context({
        'user': request.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,
        'msg_error': 'Lo sentimos, no se encuentra registrado en nuestro sistema',
        })  
        return render_to_response(plantilla, variables, context_instance=RequestContext(request))
    else:
        if user.is_active:
            auth.login(request, user)   
            return HttpResponseRedirect("/")
        else:        
            variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'msg_error': 'Lo sentimos, usted se encuentra temporalmente desabilitado',
            })  
            return render_to_response(plantilla, variables, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)    
    return HttpResponseRedirect("/")