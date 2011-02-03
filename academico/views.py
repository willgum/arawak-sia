# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                             # se incorporo para poder acceder a archivos estaticos
from django.conf import settings    
from django.contrib import auth                                                     # se incopora para poder acceder a los valores creados en el settings
from academico.models import Profesor, Estudiante, Competencia, Programa, MatriculaPrograma, Calificacion, Ciclo, Corte, Curso, MatriculaCiclo, CicloForm
from django.contrib.auth.decorators import login_required                           # me permite usar eö @login_requerid

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
def cortes(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
            competencias = Competencia.objects.filter(curso__profesor = usuario.id).distinct()
            datos = {'competencias': competencias,
                     'cantidad': len(competencias)}
        return redireccionar('academico/competencias.html', solicitud, datos)
    else:
        logout(solicitud)
            
def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")

@login_required
def promocion_ciclo(solicitud, ciclo_id):
    if solicitud.method == 'POST':
        formset = CicloForm(solicitud.POST)
        if formset.is_valid():
            formset.save()
            
            tmp_ciclo = Ciclo.objects.get(codigo = solicitud.POST['codigo'])
            tmp_fecha = solicitud.POST['fecha_inicio']
            tmp_fecha_ini = tmp_fecha[6:10] + "-" + tmp_fecha[3:5] + "-" + tmp_fecha[0:2]
    
            #Duplicar los cortes de un ciclo anterior a un ciclo nuevo
            cortes = Corte.objects.filter(ciclo = ciclo_id)
            for corte in cortes:
                tmp_corte = Corte(ciclo_id=tmp_ciclo.id, sufijo = corte.sufijo, porcentaje=corte.porcentaje, fecha_inicio=corte.fecha_inicio, fecha_fin=corte.fecha_fin)
                tmp_corte.save()
            
            #Duplicar los cursos de un ciclo anterior a un ciclo nuevo
            cursos = Curso.objects.filter(ciclo = ciclo_id)
            for curso in cursos:
                tmp_curso = Curso(competencia_id=curso.competencia_id, ciclo_id=tmp_ciclo.id, profesor_id = curso.profesor_id, grupo=curso.grupo, esperados=curso.esperados)
                tmp_curso.save()
            
            #Duplicar las matrículas de estudiante a ciclo de un ciclo anterior a un ciclo nuevo
            matriculas = MatriculaCiclo.objects.filter(ciclo = ciclo_id)
            for matricula in matriculas:
                tmp_matricula = MatriculaCiclo(fecha_inscripcion=tmp_fecha_ini, matricula_programa_id=matricula.matricula_programa_id, ciclo_id=tmp_ciclo.id, observaciones=matricula.observaciones)
                tmp_matricula.save()
        
            solicitud.user.message_set.create(message="El ciclo fué promovido correctamente a " + tmp_ciclo.codigo + ".")
            return HttpResponseRedirect("/admin/academico/ciclo")
    else:
        formset = CicloForm()
    datos = {'formset': formset,
             'ciclo': Ciclo.objects.get(id = ciclo_id)} 
    return redireccionar('admin/promocionCiclo.html', solicitud, datos)