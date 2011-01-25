# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context                                             # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                                    # se incopora para poder acceder a los valores creados en el settings
from django.contrib.auth.models import Group
from academico.models import Profesor, Estudiante, Curso, Competencia, Programa, MatriculaPrograma, MatriculaCiclo, Calificacion
from django.contrib.auth.decorators import login_required                           # me permite usar eö @login_requerid

def comprobarPerfil(solicitud):
    respuesta = [] 
    grupos = solicitud.user.groups.all()    
    if len(grupos) > 0:
        respuesta.append({'resultado':True, 'grupos':grupos})
    else:
        respuesta.append({'resultado':False})    
    return respuesta

def buscarPerfil(grupos):
    respuesta = []       
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)    
    if grupoUsuario.id == 3 or grupoUsuario.id == 4:
        respuesta.append({'resultado':True, 'grupoUsuarioid':grupoUsuario.id})        
    else:
        respuesta.append({'resultado':False})    
    return respuesta

def redireccionar(plantilla, solicitud, datos):
    variables = {
        'user': solicitud.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,
    }
    llaves = datos.keys()
    for indice in range(0,len(llaves)):
        variables[llaves[indice]] = datos[llaves[indice]]
    variables =  Context(variables)
    return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))

@login_required
def indice(solicitud):
    datos = {}
    return redireccionar('index.html', solicitud, datos)

@login_required
def programas(solicitud):
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            if resultado[0]['grupoUsuarioid'] == 3:
                usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
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
                
                datos = {'programas': listaProgramas,
                         'cantidad': len(listaProgramas)}
            else:
                usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
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
                datos = {'programas': listaProgramas,
                         'cantidad': len(listaProgramas)}
        else:
            datos = {'msg_error': "Lo sentimos, al parecer no esta inscrito a ningun programa."}
    else:
        datos = {'msg_error': "Lo sentimos, al parecer no esta inscrito a ningun programa."}
    return redireccionar('academico/programas.html', solicitud, datos)

@login_required
def programasDetalle(solicitud, programa_id):
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            programa = Programa.objects.get(id = programa_id)
            datos = {'programa': programa}  
        else:
            datos = {'msg_error': "Lo sentimos, al parecer no esta inscrito a ningun programa."}
    else:
        datos = {'msg_error': "Lo sentimos, al parecer no esta inscrito a ningun programa."}
    return redireccionar('academico/programaDetalle.html', solicitud, datos)

@login_required
def competencias(solicitud):
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            if resultado[0]['grupoUsuarioid'] == 3:
                usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
                competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
                datos = {'competencias': competencias,
                         'cantidad': len(competencias),
                         'grupoUsuario': 3}
            else:
                usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
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
                datos = {'calificaciones': calificaciones,
                         'cantidad': len(calificaciones),
                         'grupoUsuario': 4}
        else:
            datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    else:
        datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    return redireccionar('academico/competencias.html', solicitud, datos)

@login_required
def competenciasDetalle(solicitud, competencia_id):
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            competencia = Competencia.objects.get(id = competencia_id)
            datos = {'competencia': competencia}  
        else:
            datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    else:
        datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    return redireccionar('academico/competenciaDetalle.html', solicitud, datos)

@login_required
def horarios(solicitud):
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            if resultado[0]['grupoUsuarioid'] == 3:
                usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
                cursos = Curso.objects.filter(profesor = usuario.id).distinct()
                datos = {'cursos': cursos,
                         'cantidad': len(cursos),
                         'grupoUsuario': 3}
            else:
                usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
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
                datos = {'calificaciones': calificaciones,
                         'cantidad': len(calificaciones),
                         'grupoUsuario': 4}
        else:
            datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    else:
        datos = {'msg_error': "Lo sentimos, no tiene competencias inscritas."}
    return redireccionar('academico/horarios.html', solicitud, datos)