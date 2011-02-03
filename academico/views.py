# -*- coding: utf-8 -*-
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings    
from django.contrib import auth                                                                             # se incopora para poder acceder a los valores creados en el settings
from academico.models import Profesor, Estudiante, Curso, Competencia, Programa, MatriculaPrograma, MatriculaCiclo, Calificacion, Ciclo, Corte, NotaCorte, CicloForm
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid

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
    if 'grupoUsuarioid' in solicitud.session:
        return redireccionar('index.html', solicitud, {})
    else:
        logout(solicitud)

@login_required
def programas(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        datos = {'programas': buscarProgramas(solicitud)}
        return redireccionar('academico/programas.html', solicitud, datos)
    else:
        logout(solicitud)

def buscarProgramas(solicitud):
    listaProgramas = []
    if solicitud.session['grupoUsuarioid'] == 3:
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
        programas = []
        for competencia in competencias:
            programas.append(Programa.objects.get(id = competencia.programa_id))
        for indice1 in range(0, len(programas)):
            contador = 0
            for indice2 in range(indice1, len(programas)):
                if programas[indice1].codigo == programas[indice2].codigo:
                    contador += 1
            if contador <= 1:
                listaProgramas.append(programas[indice1]);
    else:
        usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
        matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id)
        programas = []
        for matricula in matriculas:
            programas.append(Programa.objects.get(id = matricula.programa_id))
        for indice1 in range(0, len(programas)):
            contador = 0
            for indice2 in range(indice1, len(programas)):
                if programas[indice1].codigo == programas[indice2].codigo:
                    contador += 1
            if contador <= 1:
                listaProgramas.append(programas[indice1]);
    return listaProgramas

@login_required
def competencias(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
            competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
            datos = {'competencias': competencias,
                     'cantidad': len(competencias)}
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
                     'cantidad': len(calificaciones)}
        return redireccionar('academico/competencias.html', solicitud, datos)
    else:
        logout(solicitud)
    
@login_required
def competenciasDetalle(solicitud, competencia_id):
    if 'grupoUsuarioid' in solicitud.session:
        competencia = Competencia.objects.get(id = competencia_id)
        datos = {'competencia': competencia}  
        return redireccionar('academico/competenciaDetalle.html', solicitud, datos)
    else:
        logout(solicitud)
        
@login_required
def horarios(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
            cursos = Curso.objects.filter(profesor = usuario.id).distinct()
            datos = {'cursos': cursos,
                     'cantidad': len(cursos)}
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
                     'cantidad': len(calificaciones)}
        return redireccionar('academico/horarios.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def notas(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
            cursos = Curso.objects.filter(profesor = usuario.id).distinct()
            datos = {'cursos': cursos,
                     'cantidad': len(cursos)}
        return redireccionar('academico/notas.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def ingresarNota(solicitud, curso_id):
    if 'grupoUsuarioid' in solicitud.session:
        if solicitud.session['grupoUsuarioid'] == 3:
            hoy = datetime.date.today() 
            curso = Curso.objects.get(id = curso_id)
            cicloActual = Ciclo.objects.get(fecha_inicio__lt = hoy, fecha_fin__gt = hoy)
            cortes = Corte.objects.filter(ciclo = cicloActual.id).order_by('fecha_inicio')         
            calificaciones = Calificacion.objects.filter(curso = curso_id) # buscar como filtrar con un metodo definido en la clase
            calificacionesCiclo = []
            for indice in calificaciones:                
                if Calificacion.cicloActual(indice):
                    notas = {}
                    notas['id'] =                   indice.id
                    notas['matricula_ciclo'] =      indice.matricula_ciclo
                    notas['nota_definitiva'] =      indice.nota_definitiva
                    notas['nota_habilitacion'] =    indice.nota_habilitacion
                    notas['fallas'] =               indice.fallas
                    notas['codigo_estudiante'] =    Calificacion.codigo_estudiante(indice)
                    notas['nombre_estudiante'] =    Calificacion.nombre_estudiante(indice)
                    notas['codigo_ciclo'] =         Calificacion.codigo_ciclo(indice)
                    for corte in cortes:
                        try:
                            resultado = NotaCorte.objects.get(calificacion = indice.id, corte = corte.id)
                            notas[corte.id] = {'nota': resultado.nota, 'fallas': resultado.fallas}
                        except:
                            notas[corte.id] = {'nota': 0, 'fallas': 0}
                    calificacionesCiclo.append(notas)               
            datos = {'curso': curso,
                     'cortes': cortes,
                     'calificaciones': calificacionesCiclo,
                     'cantidad': len(calificacionesCiclo),
                     'cantidadCortes': 5+(len(cortes)*2)}
        return redireccionar('academico/ingresarNotas.html', solicitud, datos)
    else:
        logout(solicitud)
    
def guardarNota(request):
    if request.POST:
        idCalificacion = request.POST.get('idCalificacion')
        idCorte = request.POST.get('idCorte')
        valor = request.POST.get('valor')            
        notascorte = []
        try:
            notascorte = NotaCorte.objects.get(calificacion = idCalificacion, corte = idCorte)
            notascorte.nota = valor
        except:
            notascorte = NotaCorte(calificacion_id = idCalificacion, corte_id = idCorte, nota = valor, fallas = 0, comportamiento_id = 1)
        notascorte.save()
        calificacion = Calificacion.objects.get(id = idCalificacion) 
        diccionario = {calificacion: calificacion}
        datos = serializers.serialize("json", diccionario)
        return HttpResponse(datos) 

def guardarFallas(request):
    if request.POST:
        idCalificacion = request.POST.get('idCalificacion')
        idCorte = request.POST.get('idCorte')
        valor = request.POST.get('valor')            
        notascorte = []
        try:
            notascorte = NotaCorte.objects.get(calificacion = idCalificacion, corte = idCorte)
            notascorte.fallas = valor
        except:
            notascorte = NotaCorte(calificacion_id = idCalificacion, corte_id = idCorte, nota = 0, fallas = valor, comportamiento_id = 1)
        notascorte.save()
        calificacion = Calificacion.objects.get(id = idCalificacion) 
        diccionario = {calificacion: calificacion}
        datos = serializers.serialize("json", diccionario)
        return HttpResponse(datos)
          
def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")