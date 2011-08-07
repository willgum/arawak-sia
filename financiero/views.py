# -*- coding: utf-8 -*-

# Create your views here.
from datetime import datetime, timedelta, date
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera, HoraCatedra, Ciclo, Sesion, Adelanto,  Descuento
from academico.models import Profesor, CicloForm, Institucion, Estudiante, MatriculaPrograma, MatriculaCiclo
from django.contrib.auth.decorators import login_required                                                       # me permite usar eö @login_requerid
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                                   # se incorporo para poder acceder a archivos estaticos
from django.conf import settings  
from django.contrib import auth   

#Reportes GERALDO
#from reportes import rpt_ReporteCartera, rpt_EstadoCuenta, rpt_LiquidarPagoDocente, rpt_LiquidarNominaDocente
#from geraldo.generators import PDFGenerator

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
    if solicitud.session['grupoUsuarioid'] == 3:
        return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))
    else:
        if solicitud.session['mora']:
            return render_to_response('academico/index.html', variables, context_instance=RequestContext(solicitud))
        else:
            return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))

@login_required
def indice(solicitud):
    if comprobarPermisos(solicitud):
        return redireccionar('financiero/index.html', solicitud, {})
    else:
        return logout(solicitud)
        
def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")

#----------------------------------------------vistas estudiante---------------------------------------------------------


#def buscarMatriculaProgramasEstudiante(solicitud):
#    hoy = date.today()
#    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
#    return MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)

#@login_required
#def pazySalvo(solicitud):
#    if comprobarPermisos(solicitud):
#        programas = {}
#        matProgramas = buscarMatriculaProgramasEstudiante(solicitud)        
#        for matPrograma in matProgramas:
#            aux = {}            
#            matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
#            for matCiclo in matCiclos:
#                ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id) 
#                insPros = InscripcionPrograma.objects.filter(matricula_programa = matPrograma.id)
#                for insPro in insPros:
#                    matFinans = MatriculaFinanciera.objects.filter(inscripcion_programa = insPro, ciclo = ciclo.id)
#                    for matFinan in matFinans:
#                        aux['matFinans'] = matFinan
#                        letras = LetraPagocts.filter(matricula_financiera = matFinan)
#                        aux['letras'] = letras
#                        if len(letras) > 0:
#                            aux['cantidad'] = len(letras)
#                            cantidad = 0
#                            for letra in letras:
#                                if letra.cancelada == True:
#                                    cantidad = cantidad + 1
#                            if cantidad == len(letras):
#                                aux['pazysalvo'] = True  
#                            else:
#                                aux['pazysalvo'] = False
#                        else:
#                            aux['cantidad'] = 0
#                aux['programas'] = matPrograma
#                aux['ciclo'] = ciclo
#                programas[matPrograma.id] = aux
#        datos = {'margintop': calcularMargintop(programas),
#                 'programas': programas}        
#        return redireccionar('financiero/estudiante/pazysalvo.html', solicitud, datos)
#    else:
#        return logout(solicitud)
    
#@login_required
#def pazySalvoParcial(solicitud, letra_id):
#    if comprobarPermisos(solicitud):        
#        fecha= datetime.now()
##        letra = LetraPagocts.get(id = letra_id)
#        datos = {'letra': letra,
#                 'hora': fecha.strftime("%H:%M %p"),
#                 'fecha': fecha.strftime("%d-%m-%Y"),
##                 'estudiante': Estudiante.objects.get(id_usuario = solicitud.user.id),}        
##        return redireccionar('financiero/estudiante/pazysalvoparcial.html', solicitud, datos)
#    else:
#        return logout(solicitud)
    
#@login_required
#def pazySalvoTotal(solicitud, inscripcionPrograma_id):
#    if comprobarPermisos(solicitud):        
#        fecha= datetime.now() 
#        #id_ciclo = cicloActual()
#        datos = {'hora': fecha.strftime("%H:%M %p"),
#                 'fecha': fecha.strftime("%d-%m-%Y"),
#                 #'ciclo': Ciclo.objects.get(id = id_ciclo),
#                 'estudiante': Estudiante.objects.get(id_usuario = solicitud.user.id),
##                 'inscripcionPrograma': InscripcionPrograma.objects.get(id = inscripcionPrograma_id)}        
#        return redireccionar('financiero/estudiante/pazysalvofinal.html', solicitud, datos)
#    else:
#        return logout(solicitud)
    
##@login_required
#def liquidarNomina(solicitud):
#    tmp_ciclo = CicloForm()
#    datos = {
#             'formset':tmp_ciclo,
#             } 
#    return redireccionar('admin/financiero/nomina_pago.html', solicitud, datos)

#@login_required
#def liquidarPago(solicitud, horacatedra_id):
#    tmp_horaCatedra = HoraCatedra.objects.get(id = horacatedra_id)
#    if tmp_horaCatedra:
#        tmp_profesor = Profesor.objects.get(id = tmp_horaCatedra.profesor_id)
#        tmp_ciclo = Ciclo.objects.get(id = tmp_horaCatedra.ciclo_id)
#    if solicitud.method == 'POST':
#        formPago = LiquidarPagoForm(solicitud.POST)
#        if formPago.is_valid():
#            tmp_formPago = formPago.save(commit=False)
#            sum_adelantos = 0.0
#            sum_descuentos = 0.0
#            sum_liquidado = 0.0
#            sum_sesiones = 0
#           
#            #Sumar los tiempos de sesión esperados por el docente
#            sesiones = Sesion.objects.filter(hora_catedra=horacatedra_id, fecha_sesion__range=(tmp_formPago.fecha_inicio, tmp_formPago.fecha_fin))
#            for sesion in sesiones:
#                sum_sesiones = sum_sesiones + sesion.tiempo_planeado
#            sum_liquidado = tmp_horaCatedra.valor_hora*(sum_sesiones/tmp_horaCatedra.tiempo_hora)
#            
#            #Sumar adelantos realizados al docente
#            adelantos = Adelanto.objects.filter(hora_catedra=horacatedra_id, fecha_adelanto__range=(tmp_formPago.fecha_inicio, tmp_formPago.fecha_fin))
#            for adelanto in adelantos:
#                sum_adelantos = sum_adelantos + adelanto.valor
#           
#            #Sumar descuentos realizados al valor liquidado del docente
#            descuentos = Descuento.objects.filter(hora_catedra=horacatedra_id)
#            for descuento in descuentos:
#                sum_descuentos = sum_descuentos + (sum_liquidado*(descuento.porcentaje*0.01))
#            tmp_formPago.horas_sesiones = sum_sesiones
#            tmp_formPago.valor_liquidado = sum_liquidado
#            tmp_formPago.valor_adelanto = sum_adelantos
#            tmp_formPago.valor_descuento = sum_descuentos
#            if tmp_formPago.valor_liquidado == 0:
#                solicitud.user.message_set.create(message="No se ha realizado la liquidación. No hay valor para liquidar.")
#                return  HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id + "")
#            else:
#                tmp_formPago.save()
#                solicitud.user.message_set.create(message="La liquidación se ha realizado correctamente.")
#                return  HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id + "/rpt_imprimirpago/" + tmp_formPago.recibo)
#    else:
#        formPago = LiquidarPagoForm()
#    datos = {'formpago': formPago,
#             'profesor': tmp_profesor,
#             'ciclo': tmp_ciclo,
#             'sesion': Sesion.objects.filter(hora_catedra = horacatedra_id),
#             'adelanto': Adelanto.objects.filter(hora_catedra = horacatedra_id),
#             'horacatedra': HoraCatedra.objects.get(id = horacatedra_id),
#             'liquidarpago': LiquidarPago.objects.filter(hora_catedra = horacatedra_id),} 
#    return redireccionar('admin/financiero/liquidar_pago.html', solicitud, datos)

#===============================================================================
# REPORTES DE APLICACIÓN FINANCIERA
#===============================================================================

#@login_required
#def reporteCartera(solicitud):
#    resp = HttpResponse(mimetype='application/pdf')
#    
#    tmp_matriculafinanciera = MatriculaFinanciera.objects.filter(paz_y_salvo=False).order_by('inscripcion_programa__matricula_programa__programa')
#    if tmp_matriculafinanciera:
#        reporte = rpt_ReporteCartera(queryset=tmp_matriculafinanciera)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/matriculafinanciera")
    

#@login_required
#def reporteEstadoCuenta(solicitud, matriculafinanciera_id):
#    resp = HttpResponse(mimetype='application/pdf')
#    
#    tmp_estadoCuenta = MatriculaFinanciera.objects.filter(id=matriculafinanciera_id)
#    if tmp_estadoCuenta:
#        reporte = rpt_EstadoCuenta(queryset=tmp_estadoCuenta)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/matriculafinanciera")
    

#@login_required
#def reporteLiquidarNomina(solicitud):
#    resp = HttpResponse(mimetype='application/pdf')
#    tmp_fecha = solicitud.POST['fecha_inicio']
#    fecha_inicio = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
#    tmp_fecha = solicitud.POST['fecha_fin']
#    fecha_fin = date(int(tmp_fecha[6:10]), int(tmp_fecha[3:5]), int(tmp_fecha[0:2]))
#            
#    tmp_liquidarPago = LiquidarPago.objects.filter(fecha_liquidacion__range=(fecha_inicio, fecha_fin))
#    if tmp_liquidarPago:
#        reporte = rpt_LiquidarNominaDocente(queryset=tmp_liquidarPago)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/horacatedra/")


#@login_required
#def reporteLiquidarPago(solicitud, horacatedra_id, recibo):
#    resp = HttpResponse(mimetype='application/pdf')
#    
#    tmp_liquidarPago = LiquidarPago.objects.filter(hora_catedra=horacatedra_id, recibo=recibo)
#    if tmp_liquidarPago:
#        reporte = rpt_LiquidarPagoDocente(queryset=tmp_liquidarPago)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id)
    
#@login_required
#def reporteHistorialPago(solicitud, horacatedra_id):
#    resp = HttpResponse(mimetype='application/pdf')
#    
#    tmp_liquidarPago = LiquidarPago.objects.filter(hora_catedra=horacatedra_id)
#    if tmp_liquidarPago:
#        reporte = rpt_LiquidarPagoDocente(queryset=tmp_liquidarPago)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id)