# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group
from academico.models import Profesor, Estudiante, Curso, Competencia, Programa, MatriculaPrograma, Periodicidad
from django.contrib.auth.decorators import login_required                           # me permite usar eö @login_requerid

@login_required
def programas(request):
    plantilla = "academico/programas.html",
    grupos = request.user.groups.all()    
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)
    try:
        grupoUsuario
    except:
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'msg_error': 'Lo sentimos, al parecer no esta inscrito a ningun programa.',
        })
    else:
        if grupoUsuario.id == 3 or grupoUsuario.id == 4:
            if grupoUsuario.id == 3:
                usuario = Profesor.objects.get(documento = request.user)
                programas = Programa.objects.filter(id = Competencia.objects.filter(curso__profesor = usuario.id)).distinct()
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'programas': programas,
                'cantidad': len(programas)
                })
            else:
                usuario = Estudiante.objects.get(documento = request.user)
                programas = Programa.objects.filter(id = MatriculaPrograma.objects.filter(estudiante = usuario.id)).distinct()
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'programas': programas,
                'cantidad': len(programas)
                })
        else:
            variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'msg_error': 'Lo sentimos, al parecer no esta inscrito a ningun programa.',
            }) 
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

@login_required
def programasDetalle(request, programa_id):
    plantilla = "academico/programaDetalle.html",
    grupos = request.user.groups.all()    
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)
    try:
        grupoUsuario
    except:
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'msg_error': 'Lo sentimos, no puede acceder a esta informacion.',
        })
    else:
        programa = Programa.objects.get(id = programa_id)
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'programa': programa,
            
        })  
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

@login_required
def competencias(request):
    plantilla = "academico/competencias.html",
    grupos = request.user.groups.all()    
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)
    try:
        grupoUsuario
    except:
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'msg_error': 'Lo sentimos, no tiene competencias inscritas.',
        })
    else:
        if grupoUsuario.id == 3 or grupoUsuario.id == 4:
            if grupoUsuario.id == 3:
                usuario = Profesor.objects.get(documento = request.user)
                competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'competencias': competencias,
                'cantidad': len(competencias)
                })
            else:
                usuario = Estudiante.objects.get(documento = request.user)
                programas = Programa.objects.filter(id = MatriculaPrograma.objects.filter(estudiante = usuario.id)).distinct()
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'programas': programas,
                'cantidad': len(programas)
                })
        else:
            variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'msg_error': 'Lo sentimos, no tiene competencias inscritas.',
            }) 
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))
@login_required
def competenciasDetalle(request, competencia_id):
    plantilla = "academico/competenciaDetalle.html",
    grupos = request.user.groups.all()    
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)
    try:
        grupoUsuario
    except:
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'msg_error': 'Lo sentimos, no puede acceder a esta informacion.',
        })
    else:
        competencia = Competencia.objects.get(id = competencia_id)
        variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'competencia': competencia
        })  
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))
