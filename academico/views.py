# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from datetime import datetime, timedelta, date
from django.contrib.sessions.models import Session
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                               # se incorporo para poder acceder a archivos estaticos
from django.conf import settings    
from django.contrib import auth                                                                             # se incopora para poder acceder a los valores creados en el settings
from academico.models import Profesor, Estudiante, Curso, Materia, Programa, MatriculaPrograma, MatriculaCiclo, Calificacion, Ciclo, Corte, NotaCorte, CicloForm, TipoPrograma, Institucion, MatriculaCicloForm, MatriculaProgramaForm, EstadoInscripcion, TipoNotaConceptual
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid
from django.views.decorators.csrf import csrf_exempt

#Pruebas GERALDO
from reportes import rpt_ConstanciaCiclo, rpt_EstudiantesInscritos, rpt_ConsolidadoInscritos, rpt_EstudianteCarnet
from geraldo.generators import PDFGenerator

def calcularMargintop(programas):
    i = 0
    margintop = 0
    while i < len(programas):
        margintop = margintop + 22
        i = i + 5 
    return margintop

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
    cant = 0
    intituciones = Institucion.objects.all()
    for resultado in intituciones:
        institucion = resultado
        cant = cant + 1
    if cant > 0:    
        variables = {
            'user': solicitud.user, 
            'titulo': institucion.nombre,
            'titulo_pagina': u"Sistema de Información Académica | " + institucion.nombre,
            'path': settings.MEDIA_URL,
        }
    else:
        variables = {
            'user': solicitud.user, 
            'titulo': 'Claro',
            'titulo_pagina': u"Sistema de Información Académica | Claro",
            'path': settings.MEDIA_URL,
        }    
    llaves = datos.keys()
    for indice in range(0,len(llaves)):
        variables[llaves[indice]] = datos[llaves[indice]]
    variables =  Context(variables)
    try:
        if solicitud.session['grupoUsuarioid'] == 3:
            return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))
        else:
            if solicitud.session['mora']:
                return render_to_response('academico/index.html', variables, context_instance=RequestContext(solicitud))
            else:
                return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))
    except:
        return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))
    
@login_required
def indice(solicitud):
    if comprobarPermisos(solicitud):
        return redireccionar('academico/index.html', solicitud, {})
    else:
        return logout(solicitud)

def cicloActual():
    hoy = date.today()
    return Ciclo.objects.filter(fecha_inicio__lte = hoy, fecha_fin__gte = hoy)

def cicloNuevo(solicitud):
    hoy = date.today()
    cicloNuevo = 2
    estudiante = Estudiante.objects.get(id_usuario = solicitud.user.id)
        
#    tmp_cicloNuevo = Ciclo.objects.filter(fecha_fin__gte = hoy).order_by('-fecha_fin')
    tmp_cicloNuevo = MatriculaCiclo.objects.filter(matricula_programa__estudiante = estudiante.id, ciclo__fecha_fin__gte = hoy).order_by('-ciclo__fecha_fin')
    for tmp_ciclo in tmp_cicloNuevo:
        cicloNuevo = tmp_ciclo.ciclo.id
        break
    return cicloNuevo
        
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
    listadoCursos = []
    listadoProgramas = []
    usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
    ciclos = cicloActual()         
    for ciclo in ciclos:      
        cursos = Curso.objects.filter(profesor = usuario.id, ciclo = ciclo.id)
        for curso in cursos:
            if curso not in listadoCursos:
                listadoCursos.append(curso) 
    for curso in listadoCursos:
        listadoProgramas.append(Programa.objects.get(id = curso.idPrograma()))
    for item in listadoProgramas:
        if item not in programas:
            programas.append(item)
    return programas
         
@login_required
def programasDocente(solicitud):
    if comprobarPermisos(solicitud):
        programas = buscarProgramasDocente(solicitud)
        datos = {'margintop': calcularMargintop(programas),
                 'programas': buscarProgramasDocente(solicitud)}
        return redireccionar('academico/docente/programas.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def horariosDocente(solicitud):
    if comprobarPermisos(solicitud):
        ciclos = cicloActual()
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        auxCiclo = {}
        for ciclo in ciclos:
            cursos = Curso.objects.filter(profesor = usuario.id, ciclo = ciclo.id).order_by('materia')
            auxCursos = []
            for curso in cursos:
                auxCursos.append(curso)
            if len(auxCursos) > 0:
                auxCiclo[ciclo.id] = {'ciclo': ciclo,
                                      'cursos': auxCursos, 
                                      'cantidad': len(auxCursos)}
        solicitud.session['url'] = "/academico/docente/horarios/"
        solicitud.session['link'] = "Horarios"
        datos = {'ciclo': auxCiclo,
                 'margintop': len(cursos)
                 }
        return redireccionar('academico/docente/horarios.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def notasDocente(solicitud):
    if comprobarPermisos(solicitud):
        ciclos = cicloActual()
        usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        auxCiclo = {}
        for ciclo in ciclos:
            cursos = Curso.objects.filter(profesor = usuario.id, ciclo = ciclo.id).order_by('materia')
            auxCursos = []
            for curso in cursos:
                auxCursos.append(curso)
            if len(auxCursos) > 0:
                auxCiclo[ciclo.id] = {'ciclo': ciclo,
                                      'cursos': auxCursos, 
                                      'cantidad': len(auxCursos)}
        solicitud.session['url'] = "/academico/docente/notas/"
        solicitud.session['link'] = "Calificaciones"
        datos = {'ciclo': auxCiclo,
                 'margintop': len(auxCiclo)}
        return redireccionar('academico/docente/notas.html', solicitud, datos)
    else:
        return logout(solicitud)

def calificacionNumerica(ciclo_id, curso_id):
    cortes = Corte.objects.filter(ciclo = ciclo_id).order_by('fecha_inicio')         
    calificaciones = Calificacion.objects.filter(curso = curso_id)
    calificacionesCiclo = []
    for indice in calificaciones:                
        if Calificacion.cicloActual(indice):
            notas = {}
            notas['id'] =                   indice.id
            notas['matricula_ciclo'] =      indice.matricula_ciclo
            notas['nota_definitiva'] =      indice.nota_definitiva
            notas['nota_habilitacion'] =    indice.nota_habilitacion
            notas['perdio_fallas'] =        indice.perdio_fallas
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
    datos = {'cortes': cortes,
             'calificaciones': calificacionesCiclo,
             'cantidad': len(calificacionesCiclo),
             'cantidadCortes': 5+(len(cortes)*2)}
    return datos

def calificacionConceptual(ciclo_id, curso_id):
    calificaciones = Calificacion.objects.filter(curso = curso_id)
    tipoNotas = TipoNotaConceptual.objects.all()
    valoraciones = []
    for indice in calificaciones:                
        if Calificacion.cicloActual(indice):
            notas = {}
            index = 0
            notas['id'] =                   indice.id
            notas['matricula_ciclo'] =      indice.matricula_ciclo
            notas['nota_definitiva'] =      indice.nota_definitiva
            notas['perdio_fallas'] =        indice.perdio_fallas
            notas['fallas'] =               indice.fallas
            notas['codigo_estudiante'] =    Calificacion.codigo_estudiante(indice)
            notas['nombre_estudiante'] =    Calificacion.nombre_estudiante(indice)
            notas['codigo_ciclo'] =         Calificacion.codigo_ciclo(indice)
            notas['index'] =                index
            for tipoNota in tipoNotas:
                index += 1
                numero = str(indice.nota_definitiva).split('.')
                if tipoNota.id == int(numero[0]):
                    notas['index'] = index
            valoraciones.append(notas) 
    datos = {'calificaciones': valoraciones,
             'cantidad': len(valoraciones),
             'valoraciones': tipoNotas}
    return datos

def horasBienestar(ciclo_id, curso_id):
    calificaciones = Calificacion.objects.filter(curso = curso_id)
    calificacionesCiclo = []
    for indice in calificaciones:                
        if Calificacion.cicloActual(indice):
            notas = {}
            numero = str(indice.nota_definitiva).split('.')
            notas['id'] =                   indice.id
            notas['matricula_ciclo'] =      indice.matricula_ciclo
            notas['nota_definitiva'] =      int(numero[0])
            notas['codigo_estudiante'] =    Calificacion.codigo_estudiante(indice)
            notas['nombre_estudiante'] =    Calificacion.nombre_estudiante(indice)
            notas['codigo_ciclo'] =         Calificacion.codigo_ciclo(indice)
            programa = Programa.objects.get(id = indice.idPrograma)
            matricula = MatriculaPrograma.objects.get(id = indice.idMatriculaPrograma)
            notas['horas_bienestar'] =      programa.horas_bienestar
            notas['total_horas'] =          matricula.horas_bienestar
            calificacionesCiclo.append(notas) 
    datos = {'calificaciones': calificacionesCiclo,
             'cantidad': len(calificacionesCiclo)}
    return datos
    
@login_required
def guardarNotasDocente(solicitud, ciclo_id, curso_id):
    if comprobarPermisos(solicitud):
        datos = {}
        curso = Curso.objects.get(id = curso_id)
        materia = Materia.objects.get(id = curso.idMateria)
        if materia.tipo_valoracion.id == 2:
            datos = calificacionConceptual(ciclo_id, curso_id)
            datos['curso'] = curso
            datos['val'] = materia.tipo_valoracion.id
            return redireccionar('academico/docente/notaConceptual.html', solicitud, datos)
        elif materia.tipo_valoracion.id == 3:
            datos = horasBienestar(ciclo_id, curso_id)
            datos['curso'] = curso
            datos['val'] = materia.tipo_valoracion.id
            return redireccionar('academico/docente/horasBienestar.html', solicitud, datos)
        else:
            datos = calificacionNumerica(ciclo_id, curso_id)
            datos['curso'] = curso
            datos['val'] = materia.tipo_valoracion.id
            return redireccionar('academico/docente/notaNumerica.html', solicitud, datos)
    else:
        return logout(solicitud)
        
def guardarNotaDocente(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idCalificacion = solicitud.POST.get('idCalificacion')
        idCorte = solicitud.POST.get('idCorte')
        valor = solicitud.POST.get('valor')
        try:
            notacorte = NotaCorte.objects.get(calificacion = idCalificacion, corte = idCorte)
            notacorte.nota = valor
            NotaCorte.save(notacorte)
        except:
            try:
                notacorte = NotaCorte(calificacion_id = idCalificacion, corte_id = idCorte, nota = valor, fallas = 0, comportamiento_id = 1)
                NotaCorte.save(notacorte)
            except:
                "error"
        calificacion = Calificacion.objects.filter(id = idCalificacion)
        return HttpResponse(serializers.serialize("json", calificacion), content_type = 'application/json; charset=utf8') 

def guardarFallaDocente(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idCalificacion = solicitud.POST.get('idCalificacion')
        idCorte = solicitud.POST.get('idCorte')
        valor = solicitud.POST.get('valor')  
        try:
            notacorte = NotaCorte.objects.get(calificacion = idCalificacion, corte = idCorte)
            notacorte.fallas = valor
            NotaCorte.save(notacorte)
        except:
            try:
                notacorte = NotaCorte(calificacion_id = idCalificacion, corte_id = idCorte, nota = 0, fallas = valor, comportamiento_id = 1)
                NotaCorte.save(notacorte)
            except:
                "error"
        calificacion = Calificacion.objects.filter(id = idCalificacion) 
        return HttpResponse(serializers.serialize("json", calificacion), content_type = 'application/json; charset=utf8')
    
def guardarFallas(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idCalificacion = solicitud.POST.get('idCalificacion')
        valor = solicitud.POST.get('valor')  
        calificacion = Calificacion.objects.get(id = idCalificacion)
        calificacion.fallas = valor
        Calificacion.save(calificacion)
        calificacion = Calificacion.objects.filter(id = idCalificacion) 
        return HttpResponse(serializers.serialize("json", calificacion), content_type = 'application/json; charset=utf8')
    
def guardarValoracion(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idCalificacion = solicitud.POST.get('idCalificacion')
        valor = solicitud.POST.get('valor')  
        calificacion = Calificacion.objects.get(id = idCalificacion)
        calificacion.nota_definitiva = valor
        Calificacion.save(calificacion)
        calificacion = Calificacion.objects.filter(id = idCalificacion) 
        return HttpResponse(serializers.serialize("json", calificacion), content_type = 'application/json; charset=utf8')

@csrf_exempt   
def guardarHoras(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idCalificacion = solicitud.POST.get('idCalificacion')
        valor = solicitud.POST.get('valor')  
        calificacion = Calificacion.objects.get(id = idCalificacion)
        calificacion.nota_definitiva = valor
        Calificacion.save(calificacion)
        matricula = MatriculaPrograma.objects.get(id = calificacion.idMatriculaPrograma)  
        return HttpResponse(matricula.horas_bienestar, content_type = 'application/json; charset=utf8')

@login_required
def materiasDocente(solicitud, materia_id):
    if comprobarPermisos(solicitud):
        materia = Materia.objects.get(id = materia_id)
        datos = {'materia': materia}  
        return redireccionar('academico/docente/materias.html', solicitud, datos)
    else:
        return logout(solicitud)
        
#----------------------------------------------vistas estudiante---------------------------------------------------------

def buscarProgramasEstudiante(solicitud):
    listaProgramas = []
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)
    programas = []
#    tipoPrograma = []
    for matricula in matriculas:
        vistas = 0
        aprobadas = 0        
        programas = Programa.objects.get(id = matricula.programa_id)
#        tipoPrograma = TipoPrograma.objects.get(id = programas.tipo_programa_id)
        programa = {}
        programa['codigo'] =                programas.codigo
        programa['nombre'] =                programas.nombre
        programa['abreviatura'] =           programas.abreviatura()
        programa['tipo_programa'] =         programas.tipo_programa
        programa['descripcion'] =           programas.descripcion
        programa['titulo'] =                programas.titulo
        programa['resolucion'] =            programas.resolucion
        programa['snies'] =                 programas.snies
        programa['periodicidad'] =          programas.periodicidad
        programa['duracion'] =              programas.duracion
        programa['jornada'] =               programas.jornada
        programa['materias'] =              programas.materias()
        programa['aptitudes'] =             programas.aptitudes
        programa['perfil_profesional'] =    programas.perfil_profesional
        programa['funciones'] =             programas.funciones
        matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matricula.id)
        for matCiclo in matCiclos:
            resultados = Calificacion.objects.filter(matricula_ciclo = matCiclo)
            for resultado in resultados:
                vistas = vistas + 1
#                if resultado.nota_definitiva is not None and resultado.nota_definitiva >= tipoPrograma.nota_aprobacion:
                if resultado.nota_definitiva is not None and resultado.nota_definitiva >= resultado.curso.materia.tipo_valoracion.nota_aprobacion:
                    aprobadas = aprobadas +1
        programa['vistas'] =    vistas
        programa['aprobadas'] = aprobadas       
        if aprobadas == 0 or programas.materias() == 0:
            programa['progreso'] = "images/progreso/01.png" 
            programa['porcentaje'] = 0
        else:
            progreso = (aprobadas*100)/programas.materias()
            programa['porcentaje'] = progreso 
            if progreso >= 0 and progreso <= 8.33:
                programa['progreso'] = "images/progreso/02.png"
            if progreso > 8.33 and progreso <= 16.66:
                programa['progreso'] = "images/progreso/03.png"
            if progreso > 16.66 and progreso <= 24.99:
                programa['progreso'] = "images/progreso/04.png"
            if progreso > 24.99 and progreso <= 33.32:
                programa['progreso'] = "images/progreso/05.png"
            if progreso > 33.32 and progreso <= 41.65:
                programa['progreso'] = "images/progreso/06.png"
            if progreso > 41.65 and progreso <= 49.98:
                programa['progreso'] = "images/progreso/07.png"
            if progreso > 49.98 and progreso <= 58.31:
                programa['progreso'] = "images/progreso/08.png"
            if progreso > 58.31 and progreso <= 66.64:
                programa['progreso'] = "images/progreso/09.png"        
            if progreso > 66.64 and progreso <= 74.97:
                programa['progreso'] = "images/progreso/10.png"
            if progreso > 74.97 and progreso <= 83.3:
                programa['progreso'] = "images/progreso/11.png"
            if progreso > 83.3 and progreso <= 91.63:
                programa['progreso'] = "images/progreso/12.png"
            if progreso > 91.96 and progreso <= 99.9:
                programa['progreso'] = "images/progreso/13.png"
            if progreso >= 100:
                programa['progreso'] = "images/progreso/14.png"        
        listaProgramas.append(programa)
    return listaProgramas

def buscarMatriculaProgramasEstudiante(solicitud):
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    return MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)

def buscarMateriasEstudiante(solicitud, matricula_ciclo_id):
    calificaciones = []
    resultado = Calificacion.objects.filter(matricula_ciclo = matricula_ciclo_id)                    
    if len(resultado) > 0:
        for indice in range(0, len(resultado)):
            calificaciones.append(resultado[indice])
    return calificaciones

def buscarMateriasInscribir(solicitud, ciclo, matPrograma):
    calificaciones = []
    inscripciones = []
    
    try:
        ciclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
        matCiclo = MatriculaCiclo.objects.get(matricula_programa = matPrograma.id, ciclo = ciclo.id)
        cursos = Curso.objects.filter(ciclo = ciclo.id, materia__programa = matPrograma.programa)
        
        for ciclo in ciclos:
            resultado = Calificacion.objects.filter(matricula_ciclo = ciclo.id, tipo_aprobacion__in=[1,2,3,4])
            if len(resultado) > 0:
                for indice in range(0, len(resultado)):
                    calificaciones.append(resultado[indice])
        
        for curso in cursos:
            inscripcion = {}
            existe = 0
            for calificacion in calificaciones:
                if curso.materia.id == calificacion.curso.materia.id:
                    if calificacion.tipo_aprobacion.id == 1:
                        existe = 2
                    else:
                        existe = 1
                    break
            if existe == 0:
                inscripcion['id'] = curso.materia.id
                inscripcion['id_curso'] = curso.id
                inscripcion['id_matCiclo'] = matCiclo.id
                inscripcion['codigo'] = curso.materia.codigo
                inscripcion['nombre'] = curso.materia.nombre
                inscripcion['existe'] = existe
                inscripcion['inscribir'] = "Inscribir"
                inscripciones.append(inscripcion)
            if existe == 2:
                inscripcion['id'] = curso.materia.id
                inscripcion['id_curso'] = curso.id
                inscripcion['id_matCiclo'] = matCiclo.id
                inscripcion['codigo'] = curso.materia.codigo
                inscripcion['nombre'] = curso.materia.nombre
                inscripcion['existe'] = existe
                inscripcion['inscribir'] = "Inscrita"
                inscripciones.append(inscripcion)
    except:
        inscripciones = []
        
    return inscripciones

def buscarMateriasHistorialEstudiante(solicitud):
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
        programas = buscarProgramasEstudiante(solicitud)
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas}
        return redireccionar('academico/estudiante/programas.html', solicitud, datos)
    else:
        return logout(solicitud)
               
@login_required
def horariosEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        ciclo = 0 
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
            for matCiclo in matCiclos:
                tmp_ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id)
                if Ciclo.cicloActual(tmp_ciclo):
                    ciclo = tmp_ciclo
                    aux['ciclo'] = matCiclo
                    resultado = buscarMateriasEstudiante(solicitud, matCiclo.id) 
                    aux['calificaciones'] = resultado
                    aux['cantCalificaciones'] = len(resultado)
            programas[matPrograma.id] = aux
        solicitud.session['url'] = "/academico/estudiante/horarios/"
        solicitud.session['link'] = "Horarios"
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas,
                 'ciclo': ciclo}
        return redireccionar('academico/estudiante/horarios.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def notasEstudiante(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        cortes = {}
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
            for matCiclo in matCiclos:
                tmp_ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id) 
                cortes = Corte.objects.filter(ciclo = tmp_ciclo.id).order_by('fecha_inicio')
                if Ciclo.cicloActual(tmp_ciclo):
                    ciclo = tmp_ciclo
                    aux['ciclo'] = matCiclo
                    calificaciones = buscarMateriasEstudiante(solicitud, matCiclo.id) 
                    calificacionesCiclo = []
                    for indice in calificaciones:            
                        notas = {}
                        notas['id'] =                   indice.id
                        notas['idMateria'] =            Calificacion.idMateria(indice)
                        notas['codigoMateria'] =        Calificacion.codigoMateria(indice)
                        notas['nombreMateria'] =        Calificacion.nombre_materia(indice)
                        notas['matricula_ciclo'] =      indice.matricula_ciclo
                        notas['nota_definitiva'] =      indice.nota_definitiva
                        notas['nota_habilitacion'] =    indice.nota_habilitacion
                        notas['tipo_aprobacion'] =      Calificacion.abreviatura_aprobacion(indice)
                        notas['fallas'] =               indice.fallas
                        for corte in cortes:
                            try:
                                resultado = NotaCorte.objects.get(calificacion = indice.id, corte = corte.id)
                                notas[corte.id] = {'nota': resultado.nota, 'fallas': resultado.fallas}
                            except:
                                notas[corte.id] = {'nota': 0, 'fallas': 0}
                        calificacionesCiclo.append(notas)
                    aux['ciclo'] = ciclo
                    aux['cortes'] = cortes
                    aux['calificaciones'] = calificacionesCiclo
                    aux['cantCalificaciones'] = len(calificacionesCiclo)
            programas[matPrograma.id] = aux
        solicitud.session['url'] = "/academico/estudiante/notas/"
        solicitud.session['link'] = "Calificaciones"
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas,
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
                resultado = buscarMateriasEstudiante(solicitud, matCiclo.id) 
                ciclo[matCiclo.id] = {'ciclo': matCiclo,
                                      'codigoCiclo': resCiclo,
                                      'calificaciones': resultado,
                                      'cantCalificaciones': len(resultado)}
            aux['ciclos'] = ciclo
            programas[matPrograma.id] = aux
        solicitud.session['url'] = "/academico/estudiante/historial/"
        solicitud.session['link'] = "Historial Académico"
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas}
        return redireccionar('academico/estudiante/historial.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def materiasDetalleEstudiante(solicitud, materia_id):
    if comprobarPermisos(solicitud):
        materia = Materia.objects.get(id = materia_id)
        datos = {'materia': materia}  
        return redireccionar('academico/estudiante/materias.html', solicitud, datos)
    else:
        return logout(solicitud)

@login_required
def inscripcionMaterias(solicitud):
    if comprobarPermisos(solicitud):
        programas = {}
        ciclo = Ciclo.objects.get(id = cicloNuevo(solicitud))
        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
        for matPrograma in matProgramas:
            aux = {}
            aux['programas'] = matPrograma
            aux['ciclo'] = ciclo
            
            resultado = buscarMateriasInscribir(solicitud, ciclo, matPrograma) 
            aux['calificaciones'] = resultado
            aux['cantCalificaciones'] = len(resultado)
            programas[matPrograma.id] = aux
        solicitud.session['url'] = "/academico/estudiante/horarios/"
        solicitud.session['link'] = "Horarios"
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas,
                 'ciclo': ciclo}
        return redireccionar('academico/estudiante/inscripcion.html', solicitud, datos)
    else:
        return logout(solicitud)


def inscribirMateria(solicitud):
    if solicitud.POST:
        c = {}
        texto = "vacia"
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
        idMatCiclo = solicitud.POST.get('idMatCiclo')
        curso_id = solicitud.POST.get('curso_id')
        inscribir = solicitud.POST.get('inscribir')
        
        try:
            if inscribir == "1":
                tmp_inscripcion = Calificacion(curso_id=curso_id, matricula_ciclo_id=idMatCiclo)
                tmp_inscripcion.save()
                texto = "Guardó"
            else:
                tmp_inscripcion = Calificacion.objects.get(curso = curso_id, matricula_ciclo = idMatCiclo)
                tmp_inscripcion.delete();
                texto = "Eliminó"
        except:
            texto = "error"
        return HttpResponse(texto)          

#----------------------------------------------vistas administrativas---------------------------------------------------------

@login_required
def promocion_ciclo(solicitud, ciclo_id):
    if solicitud.method == 'POST':
        formset = CicloForm(solicitud.POST)
        if formset.is_valid():
            formset.save()
            
            tmp_ciclo = Ciclo.objects.get(codigo = solicitud.POST['codigo'])
            tmp_fecha = solicitud.POST['fecha_inicio']
            tmp_fecha_ini = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
            
            tmp_fecha = solicitud.POST['fecha_fin']
            tmp_fecha_fin = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
    
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

                nva_fecha_ini = corte.fecha_inicio + timedelta(days=tmp_suma_fecha.days)
                nva_fecha_fin = corte.fecha_fin + timedelta(days=tmp_suma_fecha.days)
                
                i = i+1
                if i==len(cortes):
                    nva_fecha_fin = tmp_fecha_fin
                tmp_corte = Corte(ciclo_id=tmp_ciclo.id, sufijo = corte.sufijo, porcentaje=corte.porcentaje, fecha_inicio=nva_fecha_ini, fecha_fin=nva_fecha_fin)
                tmp_corte.save()
            
            #Duplicar los cursos de un ciclo anterior a un ciclo nuevo
            cursos = Curso.objects.filter(ciclo = ciclo_id)
            for curso in cursos:
                tmp_curso = Curso(materia_id=curso.materia_id, ciclo_id=tmp_ciclo.id, profesor_id = curso.profesor_id, grupo=curso.grupo, esperados=curso.esperados)
                tmp_curso.save()
            
            #Duplicar las matrículas de estudiante a ciclo de un ciclo anterior a un ciclo nuevo
            try:
                estado = EstadoInscripcion.objects.get(codigo=6)
            except EstadoInscripcion.DoesNotExist:
                estado = ""
            matriculas = MatriculaCiclo.objects.filter(ciclo = ciclo_id)
            for matricula in matriculas:
                tmp_matricula = MatriculaCiclo(fecha_inscripcion=tmp_fecha_ini, matricula_programa_id=matricula.matricula_programa_id, ciclo_id=tmp_ciclo.id, observaciones=matricula.observaciones)
                tmp_matricula.save()
                try:
                    tmp_matriculaPrograma = MatriculaPrograma.objects.get(id = matricula.matricula_programa_id, estado = 1)
                    tmp_matriculaPrograma.estado = estado
                    tmp_matriculaPrograma.save()
                except MatriculaPrograma.DoesNotExist:
                    tmp_matriculaPrograma = ""
        
            solicitud.user.message_set.create(message="El ciclo fue promovido correctamente.")
            return HttpResponseRedirect("/admin/academico/ciclo")
    else:
        formset = CicloForm()
    datos = {'formset': formset,
             'ciclo': Ciclo.objects.get(id = ciclo_id)} 
    return redireccionar('admin/academico/promocionCiclo.html', solicitud, datos)

@login_required
def reporteInscritos(solicitud):
    formset = MatriculaCicloForm()
    formprogramas = MatriculaProgramaForm()
    datos = {'formset': formset,
             'formprogramas': formprogramas,
             }
    return redireccionar('admin/academico/reporteInscritos.html', solicitud, datos)

#----------------------------------------------vistas reportes administrativos ---------------------------------------------------------

@login_required
def constanciaMatriculaCiclo(solicitud, matriculaciclo_id):
    resp = HttpResponse(mimetype='application/pdf')

    tmp_matriculaciclo = MatriculaCiclo.objects.filter(id=matriculaciclo_id).order_by('fecha_inscripcion')
    reporte = rpt_ConstanciaCiclo(queryset=tmp_matriculaciclo)
    reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")

    return resp

@login_required
def estudianteCarnet(solicitud, matriculaprograma_id):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_estudiante = MatriculaPrograma.objects.filter(id=matriculaprograma_id)
    reporte = rpt_EstudianteCarnet(queryset=tmp_estudiante)
    reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")

    return resp

@login_required
def detalleInscritos(solicitud):
    resp = HttpResponse(mimetype='application/pdf')
    ciclo_id = solicitud.POST['ciclo']
    programa_id = solicitud.POST['programa']
    estado_id = solicitud.POST['estado']
    
    if programa_id != "" and estado_id != "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, matricula_programa__estado=estado_id, ciclo=ciclo_id)
    if programa_id == "" and estado_id != "" and ciclo_id != "":
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__estado=estado_id, ciclo=ciclo_id)
    if programa_id != "" and estado_id == "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, ciclo=ciclo_id)
    if programa_id != "" and estado_id != "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, matricula_programa__estado=estado_id)
    if programa_id == "" and estado_id == "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(ciclo=ciclo_id)
    if programa_id == "" and estado_id != "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__estado=estado_id)
    if programa_id != "" and estado_id == "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id)
    if programa_id == "" and estado_id == "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter()
    
    if tmp_matriculaprograma:
        reporte = rpt_EstudiantesInscritos(queryset=tmp_matriculaprograma.order_by('matricula_programa__programa__nombre', 'matricula_programa__estudiante__apellido1', 'matricula_programa__estudiante__apellido2', 'matricula_programa__estudiante__nombre1', 'matricula_programa__estudiante__nombre2'))
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/academico/matriculaprograma/inscritos/")
#    tmp_matriculaprograma = MatriculaPrograma.objects.order_by('programa__nombre', 'estado', 'estudiante__apellido1', 'estudiante__apellido2', 'estudiante__nombre2')
#    reporte = rpt_EstudiantesInscritos(queryset=tmp_matriculaprograma)
#    reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#
    return resp

@login_required
def consolidadoInscritos(solicitud):
    resp = HttpResponse(mimetype='application/pdf')
    ciclo_id = solicitud.POST['ciclo']
    programa_id = solicitud.POST['programa']
    estado_id = solicitud.POST['estado']
    
    if programa_id != "" and estado_id != "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, matricula_programa__estado=estado_id, ciclo=ciclo_id).order_by('matricula_programa__programa__nombre')
    if programa_id == "" and estado_id != "" and ciclo_id != "":
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__estado=estado_id, ciclo=ciclo_id).order_by('matricula_programa__programa__nombre')
    if programa_id != "" and estado_id == "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, ciclo=ciclo_id).order_by('matricula_programa__programa__nombre')
    if programa_id != "" and estado_id != "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id, matricula_programa__estado=estado_id).order_by('matricula_programa__programa__nombre')
    if programa_id == "" and estado_id == "" and ciclo_id != "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(ciclo=ciclo_id).order_by('matricula_programa__programa__nombre')
    if programa_id == "" and estado_id != "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__estado=estado_id).order_by('matricula_programa__programa__nombre')
    if programa_id != "" and estado_id == "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter(matricula_programa__programa=programa_id).order_by('matricula_programa__programa__nombre')
    if programa_id == "" and estado_id == "" and ciclo_id == "":   
        tmp_matriculaprograma = MatriculaCiclo.objects.filter().order_by('matricula_programa__programa__nombre')
    
    if tmp_matriculaprograma:
        reporte = rpt_ConsolidadoInscritos(queryset=tmp_matriculaprograma)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/academico/matriculaprograma/inscritos/")
    return resp