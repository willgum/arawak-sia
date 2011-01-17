# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib.auth.decorators import login_required       # me permite usar eö @login_requerid

@login_required
def indice(request):
    plantilla = "academico/index.html",
    variables = Context({
        'user': request.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,  
    })
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))