# -*- coding: utf-8 -*-

# Create your views here.
from datetime import datetime, timedelta, date
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera, HoraCatedra, Ciclo, Sesion, Adelanto, LiquidarPago, LiquidarPagoForm, Descuento
from academico.models import Profesor, CicloForm, Institucion, Corte, MatriculaCiclo, Calificacion, NotaCorte, Estudiante, MatriculaPrograma, Programa, TipoPrograma
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                                        # se incorporo para poder acceder a archivos estaticos
from django.conf import settings  
from django.contrib import auth   

#Reportes GERALDO
from reportes import rpt_ReporteCartera, rpt_EstadoCuenta, rpt_LiquidarPagoDocente, rpt_LiquidarNominaDocente

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
    intituciones = Institucion.objects.all()
    for resultado in intituciones:
        institucion = resultado
    variables = {
        'user': solicitud.user, 
        'titulo': '.: ' + institucion.nombre + ' :.',
        'titulo_pagina': '.: ' + institucion.nombre + ' :.',
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
        return redireccionar('financiero/index.html', solicitud, {})
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

#----------------------------------------------vistas estudiante---------------------------------------------------------

def buscarProgramasEstudiante(solicitud):
    listaProgramas = []
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    matriculas = MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)
    programas = []
    tipoPrograma = []
    for matricula in matriculas:
        vistas = 0
        aprobadas = 0        
        programas = Programa.objects.get(id = matricula.programa_id)
        tipoPrograma = TipoPrograma.objects.get(id = programas.tipo_programa_id)
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
        programa['competencias'] =          programas.competencias()
        programa['actitudes'] =             programas.actitudes
        programa['perfil_profesional'] =    programas.perfil_profesional
        programa['funciones'] =             programas.funciones
        matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matricula.id)
        for matCiclo in matCiclos:
            resultados = Calificacion.objects.filter(matricula_ciclo = matCiclo)
            for resultado in resultados:
                vistas = vistas + 1
                if resultado.nota_definitiva is not None and resultado.nota_definitiva >= tipoPrograma.nota_aprobacion:
                    aprobadas = aprobadas +1
        programa['vistas'] =    vistas
        programa['aprobadas'] = aprobadas
       
        if aprobadas == 0 or programas.competencias() == 0:
            programa['progreso'] = "images/progreso/00.png" 
        else:
            progreso = (aprobadas*100)/programas.competencias()
             
            if progreso > 0 and progreso <= 7.14:
                programa['progreso'] = "images/progreso/01.png"
            if progreso > 7.14 and progreso <= 14.28:
                programa['progreso'] = "images/progreso/01.png"
            if progreso > 14.28 and progreso <= 14.28:
                programa['progreso'] = "images/progreso/02.png"
            if progreso > 7.14 and progreso <= 24.42:
                programa['progreso'] = "images/progreso/03.png"
            if progreso > 21.42 and progreso <= 28.56:
                programa['progreso'] = "images/progreso/04.png"
            if progreso > 28.56 and progreso <= 35.7:
                programa['progreso'] = "images/progreso/05.png"
            if progreso > 35.7 and progreso <= 42.84:
                programa['progreso'] = "images/progreso/06.png"
            if progreso > 42.84 and progreso <= 49.98:
                programa['progreso'] = "images/progreso/07.png"        
            if progreso > 49.98 and progreso <= 57.12:
                programa['progreso'] = "images/progreso/08.png"
            if progreso > 57.12 and progreso <= 64.26:
                programa['progreso'] = "images/progreso/09.png"
            if progreso > 64.26 and progreso <= 71.4:
                programa['progreso'] = "images/progreso/10.png"
            if progreso > 71.4 and progreso <= 78.54:
                programa['progreso'] = "images/progreso/11.png"
            if progreso > 78.54 and progreso <= 85.68:
                programa['progreso'] = "images/progreso/12.png"
            if progreso > 85.68 and progreso <= 100:
                programa['progreso'] = "images/progreso/13.png"
            if progreso >= 100:
                programa['progreso'] = "images/progreso/14.png"
        
        listaProgramas.append(programa)
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
def pazySalvo(solicitud):
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
                        notas['nombreCompetencia'] =    Calificacion.nombre_competencia(indice)
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
                    aux['calificaciones'] = calificacionesCiclo
                    aux['cantCalificaciones'] = len(calificacionesCiclo)
            programas[matPrograma.id] = aux
        solicitud.session['url'] = "/academico/estudiante/notas/"
        solicitud.session['link'] = "Calificaciones"
        datos = {'margintop': calcularMargintop(programas),
                 'programas': programas,
                 'ciclo': ciclo,
                 'cortes': cortes,
                 'cantCortes': (len(cortes)*2)+5}        
        return redireccionar('financiero/estudiante/pazysalvo.html', solicitud, datos)
    else:
        return logout(solicitud)
    
@login_required
def liquidarNomina(solicitud):
    tmp_ciclo = CicloForm()
    datos = {
             'formset':tmp_ciclo,
             } 
    return redireccionar('admin/financiero/nomina_pago.html', solicitud, datos)

@login_required
def liquidarPago(solicitud, horacatedra_id):
    tmp_horaCatedra = HoraCatedra.objects.get(id = horacatedra_id)
    if tmp_horaCatedra:
        tmp_profesor = Profesor.objects.get(id = tmp_horaCatedra.profesor_id)
        tmp_ciclo = Ciclo.objects.get(id = tmp_horaCatedra.ciclo_id)
    if solicitud.method == 'POST':
        formPago = LiquidarPagoForm(solicitud.POST)
        if formPago.is_valid():
            tmp_formPago = formPago.save(commit=False)
            sum_adelantos = 0.0
            sum_descuentos = 0.0
            sum_liquidado = 0.0
            sum_sesiones = 0
           
            #Sumar los tiempos de sesión esperados por el docente
            sesiones = Sesion.objects.filter(hora_catedra=horacatedra_id, fecha_sesion__range=(tmp_formPago.fecha_inicio, tmp_formPago.fecha_fin))
            for sesion in sesiones:
                sum_sesiones = sum_sesiones + sesion.tiempo_planeado
            sum_liquidado = tmp_horaCatedra.valor_hora*(sum_sesiones/tmp_horaCatedra.tiempo_hora)
            
            #Sumar adelantos realizados al docente
            adelantos = Adelanto.objects.filter(hora_catedra=horacatedra_id, fecha_adelanto__range=(tmp_formPago.fecha_inicio, tmp_formPago.fecha_fin))
            for adelanto in adelantos:
                sum_adelantos = sum_adelantos + adelanto.valor
           
            #Sumar descuentos realizados al valor liquidado del docente
            descuentos = Descuento.objects.filter(hora_catedra=horacatedra_id)
            for descuento in descuentos:
                sum_descuentos = sum_descuentos + (sum_liquidado*(descuento.porcentaje*0.01))
            tmp_formPago.horas_sesiones = sum_sesiones
            tmp_formPago.valor_liquidado = sum_liquidado
            tmp_formPago.valor_adelanto = sum_adelantos
            tmp_formPago.valor_descuento = sum_descuentos
            if tmp_formPago.valor_liquidado == 0:
                solicitud.user.message_set.create(message="No se ha realizado la liquidación. No hay valor para liquidar.")
                return  HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id + "")
            else:
                tmp_formPago.save()
                solicitud.user.message_set.create(message="La liquidación se ha realizado correctamente.")
                return  HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id + "/rpt_imprimirpago/" + tmp_formPago.recibo)
    else:
        formPago = LiquidarPagoForm()
    datos = {'formpago': formPago,
             'profesor': tmp_profesor,
             'ciclo': tmp_ciclo,
             'sesion': Sesion.objects.filter(hora_catedra = horacatedra_id),
             'adelanto': Adelanto.objects.filter(hora_catedra = horacatedra_id),
             'horacatedra': HoraCatedra.objects.get(id = horacatedra_id),
             'liquidarpago': LiquidarPago.objects.filter(hora_catedra = horacatedra_id),} 
    return redireccionar('admin/financiero/liquidar_pago.html', solicitud, datos)

#===============================================================================
# REPORTES DE APLICACIÓN FINANCIERA
#===============================================================================

@login_required
def reporteCartera(solicitud):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_matriculafinanciera = MatriculaFinanciera.objects.filter(paz_y_salvo=False).order_by('inscripcion_programa__matricula_programa__programa')
    if tmp_matriculafinanciera:
        reporte = rpt_ReporteCartera(queryset=tmp_matriculafinanciera)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
        return resp
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/financiero/matriculafinanciera")
    

@login_required
def reporteEstadoCuenta(solicitud, matriculafinanciera_id):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_estadoCuenta = MatriculaFinanciera.objects.filter(id=matriculafinanciera_id)
    if tmp_estadoCuenta:
        reporte = rpt_EstadoCuenta(queryset=tmp_estadoCuenta)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
        return resp
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/financiero/matriculafinanciera")
    

@login_required
def reporteLiquidarNomina(solicitud):
    resp = HttpResponse(mimetype='application/pdf')
    tmp_fecha = solicitud.POST['fecha_inicio']
    fecha_inicio = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
    tmp_fecha = solicitud.POST['fecha_fin']
    fecha_fin = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
            
    tmp_liquidarPago = LiquidarPago.objects.filter(fecha_liquidacion__range=(fecha_inicio, fecha_fin))
    if tmp_liquidarPago:
        reporte = rpt_LiquidarNominaDocente(queryset=tmp_liquidarPago)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
        return resp
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/financiero/horacatedra/")


@login_required
def reporteLiquidarPago(solicitud, horacatedra_id, recibo):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_liquidarPago = LiquidarPago.objects.filter(hora_catedra=horacatedra_id, recibo=recibo)
    if tmp_liquidarPago:
        reporte = rpt_LiquidarPagoDocente(queryset=tmp_liquidarPago)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
        return resp
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id)
    
@login_required
def reporteHistorialPago(solicitud, horacatedra_id):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_liquidarPago = LiquidarPago.objects.filter(hora_catedra=horacatedra_id)
    if tmp_liquidarPago:
        reporte = rpt_LiquidarPagoDocente(queryset=tmp_liquidarPago)
        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
        return resp
    else:
        solicitud.user.message_set.create(message="No existe datos para mostrar.")
        return HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id)