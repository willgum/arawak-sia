# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera, HoraCatedra, Ciclo, Sesion, Adelanto, LiquidarPago, LiquidarPagoForm, Descuento
from academico.models import Profesor, CicloForm
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                                        # se incorporo para poder acceder a archivos estaticos
from django.conf import settings
from datetime import date
    
#Reportes GERALDO
from reportes import rpt_ReporteCartera, rpt_EstadoCuenta, rpt_LiquidarPagoDocente, rpt_LiquidarNominaDocente

from geraldo.generators import PDFGenerator

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