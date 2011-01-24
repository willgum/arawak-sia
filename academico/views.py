# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group
from academico.models import Profesor, Estudiante, Curso, Competencia, Programa, MatriculaPrograma, MatriculaCiclo, Periodicidad, Calificacion
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
                competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
                
                programas = []
                for competencia in competencias:
                    programas.append(Programa.objects.get(id = competencia.programa_id))
                
                listaProgramas = []
                for indice1 in range(0, len(programas)):
                    contador = 0
                    for indice2 in range(indice1, len(programas)):
                        if programas[indice1].codigo == programas[indice2].codigo:
                            contador += 1
                    if contador <= 1:
                        listaProgramas.append(programas[indice1]);                    
                    
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'programas': listaProgramas,
                'cantidad': len(listaProgramas)
                })
            else:
                usuario = Estudiante.objects.get(documento = request.user)
                matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id)
                
                programas = []
                for matricula in matriculas:
                    programas.append(Programa.objects.get(id = matricula.programa_id))
                
                listaProgramas = []
                for indice1 in range(0, len(programas)):
                    contador = 0
                    for indice2 in range(indice1, len(programas)):
                        if programas[indice1].codigo == programas[indice2].codigo:
                            contador += 1
                    if contador <= 1:
                        listaProgramas.append(programas[indice1]);
                        
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'programas': listaProgramas,
                'cantidad': len(listaProgramas)
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
                'cantidad': len(competencias),
                'grupoUsuario': grupoUsuario.id,
                })
            else:
                usuario = Estudiante.objects.get(documento = request.user)
                matPrograma = MatriculaPrograma.objects.filter(estudiante = usuario.id)
                
                matCiclo = []
                for mat in matPrograma:
                    resultado = MatriculaCiclo.objects.filter(matricula_programa = mat.id)
                    if len(resultado) > 0:
                        for indice1 in range(0, len(resultado)):
                            contador = 0
                            if len(matCiclo) > 0:
                                for indice2 in range(0, len(matCiclo)):
                                    if resultado[indice1] == matCiclo[indice2]:
                                        contador += 1
                                    if contador == 0:
                                        matCiclo.append(resultado[indice1])
                            else:
                                matCiclo.append(resultado[indice1])
                
                calificaciones = []
                for mat in matCiclo:
                    resultado = Calificacion.objects.filter(matricula_ciclo = mat.id)                    
                    if len(resultado) > 0:
                        for indice in range(0, len(resultado)):
                            calificaciones.append(resultado[indice])
                                
                variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'calificaciones': calificaciones,
                'grupoUsuario': grupoUsuario.id,
                'cantidad': len(calificaciones)
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
