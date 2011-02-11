# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from django.contrib.sessions.models import Session
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings    
from django.contrib import auth                                                                             # se incopora para poder acceder a los valores creados en el settings
from academico.models import Profesor, Estudiante, Curso, Competencia, Programa, MatriculaPrograma, MatriculaCiclo, Calificacion, Ciclo, Corte, NotaCorte, CicloForm
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid

def comprobarPermisos(solicitud):
    if 'grupoUsuarioid' in solicitud.session: 
        sesion = Session.objects.get(session_key = solicitud.session.session_key)
        if  datetime.now() <= sesion.expire_date:
            sesion.expire_date = datetime.now() + timedelta(minutes=10)
            sesion.save()
        if solicitud.session['grupoUsuarioid'] == 3:
            return True
        else:
            if solicitud.session['grupoUsuarioid'] == 4:
                return True
            else:
                return False
    else:
        return False

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
    if comprobarPermisos(solicitud):
        return redireccionar('index.html', solicitud, {})
    else:
        return logout(solicitud)

def cicloActual():
    hoy = date.today()
    cicloActual = Ciclo.objects.get(fecha_inicio__lte = hoy, fecha_fin__gte = hoy)
    return cicloActual.id
        
def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")

#----------------------------------------------vistas docente---------------------------------------------------------

def buscarProgramasDocente(solicitud):
    programas = []
    listaProgramas = []
    usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
    cursos = Curso.objects.filter(profesor = usuario.id, ciclo = cicloActual())
    for curso in cursos:
        programas.append(Programa.objects.get(id = curso.idPrograma))
    for indice1 in range(0, len(programas)):
        contador = 0
        for indice2 in range(indice1, len(programas)):
            if programas[indice1].codigo == programas[indice2].codigo:
                contador += 1
        if contador <= 1:
            listaProgramas.append(programas[indice1]);
    return listaProgramas
    
@login_required
def programasDocente(solicitud):
    if comprobarPermisos(solicitud):
        datos = {'programas': buscarProgramasDocente(solicitud)}
        return redireccionar('academico/docente/programas.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def horariosDocente(solicitud):
    if comprobarPermisos(solicitud):
        id_ciclo = cicloActual()
        ciclo = Ciclo.objects.get(id = id_ciclo)
        programas = buscarProgramasDocente(solicitud)
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        cursos = Curso.objects.filter(profesor = usuario.id, ciclo = id_ciclo)
        auxProgramas = {}
        for programa in programas:
            auxCursos = {}
            for curso in cursos:          
                if curso.idPrograma() == programa.id:
                    auxCursos[curso.id] = curso
            auxProgramas[programa.id] = {'programa': programa,
                                         'cursos': auxCursos,
                                         'cantidad': len(auxCursos),}
        datos = {'programas': auxProgramas,
                 'ciclo': ciclo}
        return redireccionar('academico/docente/horarios.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def notasDocente(solicitud):
    if comprobarPermisos(solicitud):
        id_ciclo = cicloActual()
        ciclo = Ciclo.objects.get(id = id_ciclo)
        programas = buscarProgramasDocente(solicitud)
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        cursos = Curso.objects.filter(profesor = usuario.id, ciclo = id_ciclo)
        auxProgramas = {}
        for programa in programas:
            auxCursos = {}
            for curso in cursos:          
                if curso.idPrograma() == programa.id:
                    auxCursos[curso.id] = curso
            auxProgramas[programa.id] = {'programa': programa,
                                         'cursos': auxCursos,
                                         'cantidad': len(auxCursos),}
        datos = {'programas': auxProgramas,
                 'ciclo': ciclo}
        return redireccionar('academico/docente/notas.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def guardarNotasDocente(solicitud, curso_id):
    if comprobarPermisos(solicitud):
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
        return logout(solicitud)
        
def guardarNotaDocente(request):
    if request.POST:
        idCalificacion = request.POST.get('idCalificacion')
        idCorte = request.POST.get('idCorte')
        valor = request.POST.get('valor')
        notascorte = []
        try:
            notascorte = NotaCorte.objects.get(calificacion = idCalificacion, corte = idCorte)
            notascorte.nota = valor
        except NotaCorte.DoesNotExist: 
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
        except NotaCorte.DoesNotExist:
            notascorte = NotaCorte(calificacion_id = idCalificacion, corte_id = idCorte, nota = 0, fallas = valor, comportamiento_id = 1)
        notascorte.save()
        calificacion = Calificacion.objects.get(id = idCalificacion) 
        diccionario = {calificacion: calificacion}
        datos = serializers.serialize("json", diccionario)
        return HttpResponse(datos)

@login_required
def competenciasDocente(solicitud, competencia_id):
    if comprobarPermisos(solicitud):
        competencia = Competencia.objects.get(id = competencia_id)
        datos = {'competencia': competencia}  
        return redireccionar('academico/docente/competencia.html', solicitud, datos)
    else:
        return logout(solicitud)
        
#----------------------------------------------vistas estudiante---------------------------------------------------------

def buscarProgramasEstudiante(solicitud):
    listaProgramas = []
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)
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

def buscarMatriculaProgramasEstudiante(solicitud):
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    return MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)

def buscarCompetenciasEstudiante(solicitud, matricula_ciclo_id):
    calificaciones = []
    resultado = Calificacion.objects.filter(matricula_ciclo = matricula_ciclo_id)                    
    if len(resultado) > 0:
        for indice in range(0, len(resultado)):
            calificaciones.append(resultado[indice])
    return calificaciones

def buscarCompetenciasHistorialEstudiante(solicitud):
    matPrograma = buscarMatriculaProgramasEstudiante(solicitud)                
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
    return calificaciones

@login_required
def programasEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        datos = {'programas': buscarProgramasEstudiante(solicitud)}
        return redireccionar('academico/estudiante/programas.html', solicitud, datos)
    else:
        return logout(solicitud)
               
@login_required
def horariosEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        ciclo = Ciclo.objects.get(id = cicloActual())
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
            for matCiclo in matCiclos:
                ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id) 
                if Ciclo.cicloActual(ciclo):
                    aux['ciclo'] = matCiclo
                    resultado = buscarCompetenciasEstudiante(solicitud, matCiclo.id) 
                    aux['calificaciones'] = resultado
                    aux['cantCalificaciones'] = len(resultado)
            programas[matPrograma.id] = aux
        datos = {'programas': programas,
                 'ciclo': ciclo}
        return redireccionar('academico/estudiante/horarios.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def notasEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        id_ciclo = cicloActual()
        ciclo = Ciclo.objects.get(id = id_ciclo)
        cortes = Corte.objects.filter(ciclo = id_ciclo).order_by('fecha_inicio')
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
            for matCiclo in matCiclos:
                ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id) 
                if Ciclo.cicloActual(ciclo):
                    aux['ciclo'] = matCiclo
                    calificaciones = buscarCompetenciasEstudiante(solicitud, matCiclo.id) 
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
                    aux['calificaciones'] = calificacionesCiclo
                    aux['cantCalificaciones'] = len(calificacionesCiclo)
            programas[matPrograma.id] = aux
        datos = {'programas': programas,
                 'ciclo': ciclo,
                 'cortes': cortes,
                 'cantCortes': (len(cortes)*2)+5}        
        return redireccionar('academico/estudiante/notas.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def historialEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
            ciclo = {}
            for matCiclo in matCiclos:
                resCiclo  = Ciclo.objects.get(id = matCiclo.ciclo_id)
                resultado = buscarCompetenciasEstudiante(solicitud, matCiclo.id) 
                ciclo[matCiclo.id] = {'ciclo': matCiclo,
                                      'codigoCiclo': resCiclo,
                                      'calificaciones': resultado,
                                      'cantCalificaciones': len(resultado)}
            aux['ciclos'] = ciclo
            programas[matPrograma.id] = aux
        datos = {'programas': programas}
        return redireccionar('academico/estudiante/historial.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def competenciasDetalleEstudiante(solicitud, competencia_id):
    if comprobarPermisos(solicitud):
        competencia = Competencia.objects.get(id = competencia_id)
        datos = {'competencia': competencia}  
        return redireccionar('academico/estudiante/competencia.html', solicitud, datos)
    else:
        return logout(solicitud)
        
#----------------------------------------------vistas administrativas---------------------------------------------------------

@login_required
def promocion_ciclo(solicitud, ciclo_id):
    if solicitud.method == 'POST':
        formset = CicloForm(solicitud.POST)
        if formset.is_valid():
            formset.save()
            
            tmp_ciclo = Ciclo.objects.get(codigo = solicitud.POST['codigo'])
            tmp_fecha = solicitud.POST['fecha_inicio']
            tmp_fecha_ini = datetime.date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
            
            tmp_fecha = solicitud.POST['fecha_fin']
            tmp_fecha_fin = datetime.date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
    
            #Duplicar los cortes de un ciclo anterior a un ciclo nuevo
            cortes = Corte.objects.filter(ciclo = ciclo_id)
            i=0
            nva_fecha_ini = tmp_fecha_ini
            tmp_suma_fecha = 0
            #TODO: este ciclo puede optimizarse. El objetivo es que la fecha inicio de ciclo 
            #        sea la misma del primer corte y la fecha fin de ciclo sea la misma fecha fin del último corte
            for corte in cortes:
                if tmp_suma_fecha == 0:
                    tmp_suma_fecha = tmp_fecha_ini - corte.fecha_inicio

                nva_fecha_ini = corte.fecha_inicio + datetime.timedelta(days=tmp_suma_fecha.days)
                nva_fecha_fin = corte.fecha_fin + datetime.timedelta(days=tmp_suma_fecha.days)
                
                i = i+1
                if i==len(cortes):
                    nva_fecha_fin = tmp_fecha_fin
                tmp_corte = Corte(ciclo_id=tmp_ciclo.id, sufijo = corte.sufijo, porcentaje=corte.porcentaje, fecha_inicio=nva_fecha_ini, fecha_fin=nva_fecha_fin)
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
        
            solicitud.user.message_set.create(message="El ciclo fue promovido correctamente.")
            return HttpResponseRedirect("/admin/academico/ciclo")
    else:
        formset = CicloForm()
    datos = {'formset': formset,
             'ciclo': Ciclo.objects.get(id = ciclo_id)} 
    return redireccionar('admin/promocionCiclo.html', solicitud, datos)