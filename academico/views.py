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

def cicloActual():
    hoy = datetime.date.today()
    cicloActual = Ciclo.objects.get(fecha_inicio__lt = hoy, fecha_fin__gt = hoy)
    return cicloActual.id
        
def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")

#----------------------------------------------vistas docente---------------------------------------------------------

@login_required
def programasDocente(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        listaProgramas = []
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        competencias = Competencia.objects.filter(curso__profesor = usuario.id, curso__ciclo = cicloActual()).distinct()
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
        datos = {'programas': listaProgramas}
        return redireccionar('academico/docente/programas.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def competenciasDocente(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        competencias = Competencia.objects.filter(curso__profesor = usuario.id, curso__ciclo = cicloActual()).distinct()
        datos = {'competencias': competencias,
                 'cantidad': len(competencias)}        
        return redireccionar('academico/docente/competencias.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def horariosDocente(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        cursos = Curso.objects.filter(profesor = usuario.id, ciclo = cicloActual())
        datos = {'cursos': cursos,
                 'cantidad': len(cursos)}
        return redireccionar('academico/docente/horarios.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def notasDocente(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        cursos = Curso.objects.filter(profesor = usuario.id, ciclo = cicloActual())
        datos = {'cursos': cursos,
                 'cantidad': len(cursos)}
        return redireccionar('academico/docente/notas.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def guardarNotasDocente(solicitud, curso_id):
    if 'grupoUsuarioid' in solicitud.session:
        curso = Curso.objects.get(id = curso_id)
        cortes = Corte.objects.filter(ciclo = cicloActual()).order_by('fecha_inicio')         
        calificaciones = Calificacion.objects.filter(curso = curso_id)
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
        return redireccionar('academico/docente/guardarNotas.html', solicitud, datos)
    else:
        logout(solicitud)
        
def guardarNotaDocente(request):
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

def guardarFallasDocente(request):
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

@login_required
def competenciasDetalleDocente(solicitud, competencia_id):
    if 'grupoUsuarioid' in solicitud.session:
        competencia = Competencia.objects.get(id = competencia_id)
        datos = {'competencia': competencia}  
        return redireccionar('academico/docente/competenciaDetalle.html', solicitud, datos)
    else:
        logout(solicitud)
        
#----------------------------------------------vistas estudiante---------------------------------------------------------

def buscarProgramasEstudiante(solicitud):
    listaProgramas = []
    hoy = datetime.date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lt = hoy, fecha_vencimiento__gt = hoy)
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

def buscarCompetenciasEstudiante(solicitud):
    matPrograma = buscarProgramasEstudiante(solicitud)                
    matCiclo = []
    for mat in matPrograma:
        resultado = MatriculaCiclo.objects.filter(matricula_programa = mat.id, ciclo = cicloActual())
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
    return calificaciones

@login_required
def programasEstudiante(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        datos = {'programas': buscarProgramasEstudiante(solicitud)}
        return redireccionar('academico/estudiante/programas.html', solicitud, datos)
    else:
        logout(solicitud)
        
@login_required
def competenciasEstudiante(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        calificaciones = buscarCompetenciasEstudiante(solicitud)                                
        datos = {'calificaciones': calificaciones,
                 'cantidad': len(calificaciones)}
        return redireccionar('academico/estudiante/competencias.html', solicitud, datos)
    else:
        logout(solicitud)
               
@login_required
def horariosEstudiante(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        calificaciones = buscarCompetenciasEstudiante(solicitud)                                
        datos = {'calificaciones': calificaciones,
                 'cantidad': len(calificaciones)}
        return redireccionar('academico/estudiante/horarios.html', solicitud, datos)
    else:
        logout(solicitud)
    
@login_required
def notasEstudiante(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        programas = buscarProgramasEstudiante(solicitud)
        calificaciones = buscarCompetenciasEstudiante(solicitud)
        cortes = Corte.objects.filter(ciclo = cicloActual()).order_by('fecha_inicio')
        calificacionesCiclo = []
        for indice in calificaciones:            
            notas = {}
            notas['id'] =                   indice.id
            notas['idCompetencia'] =        Calificacion.idCompetencia(indice)
            notas['codigoCompetencia'] =    Calificacion.codigoCompetencia(indice)
            notas['nombreCompetencia'] =    Calificacion.nombreCompetencia(indice)
            notas['matricula_ciclo'] =      indice.matricula_ciclo
            notas['nota_definitiva'] =      indice.nota_definitiva
            notas['nota_habilitacion'] =    indice.nota_habilitacion
            notas['fallas'] =               indice.fallas
            for corte in cortes:
                try:
                    resultado = NotaCorte.objects.get(calificacion = indice.id, corte = corte.id)
                    notas[corte.id] = {'nota': resultado.nota, 'fallas': resultado.fallas}
                except:
                    notas[corte.id] = {'nota': 0, 'fallas': 0}
            calificacionesCiclo.append(notas)
        
        datos = {'cortes': cortes,                 
                 'programas': programas,
                 'calificaciones': calificacionesCiclo,
                 'cantidad': len(calificacionesCiclo),
                 'cantidadCortes': 5+(len(cortes)*2)
                 }           
        return redireccionar('academico/estudiante/notas.html', solicitud, datos)
    else:
        logout(solicitud)

@login_required
def competenciasDetalleEstudiante(solicitud, competencia_id):
    if 'grupoUsuarioid' in solicitud.session:
        competencia = Competencia.objects.get(id = competencia_id)
        datos = {'competencia': competencia}  
        return redireccionar('academico/estudiante/competenciaDetalle.html', solicitud, datos)
    else:
        logout(solicitud)
        
#----------------------------------------------vistas administrativas---------------------------------------------------------

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