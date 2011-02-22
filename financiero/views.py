# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera, HoraCatedraForm, HoraCatedra, Ciclo, Sesion, Adelanto, LiquidarPago, LiquidarPagoForm
from academico.models import Profesor
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                                                        # se incorporo para poder acceder a archivos estaticos
from django.conf import settings
from datetime import date
    
#Reportes GERALDO
from reportes import rpt_ReporteCartera, rpt_EstadoCuenta

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
def estadoCuenta(solicitud, matriculafinanciera_id):
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
def liquidarPago(solicitud, horacatedra_id):
    tmp_horaCatedra = HoraCatedra.objects.get(id = horacatedra_id)
    if tmp_horaCatedra:
        tmp_profesor = Profesor.objects.get(id = tmp_horaCatedra.profesor_id)
        tmp_ciclo = Ciclo.objects.get(id = tmp_horaCatedra.ciclo_id)
    if solicitud.method == 'POST':
        formPago = LiquidarPagoForm(solicitud.POST)
        if formPago.is_valid():
#            tmp_fecha = formPago.fecha_inicio
#            tmp_fecha_inicio = formPago.fecha_inicio
#            tmp_fecha = solicitud.POST['fecha_fin']
#            tmp_fecha_fin = formPago.fecha_fin
#            tmp_liquidarPago = LiquidarPago(hora_catedra_id=horacatedra_id, fecha_liquidacion=formPago.fecha_liquidacion)
            formPago.pago.valor_liquidado = 0
            formPago.valor_adelanto = 0
            formPago.valor_descuento = 0
            formPago.save()
#            tmp_liquidarPago.save()
#            formset.save()
            solicitud.user.message_set.create(message="El ciclo fue promovido correctamente.")
#        return HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id + "/rpt_horacatedra/")
            return  HttpResponseRedirect("/admin/financiero/horacatedra/" + horacatedra_id)
    else:
        formPago = LiquidarPagoForm()
    datos = {'formpago': formPago,
             'profesor': tmp_profesor,
             'ciclo': tmp_ciclo,
             'sesion': Sesion.objects.filter(hora_catedra = horacatedra_id),
             'adelanto': Adelanto.objects.filter(hora_catedra = horacatedra_id),
             'horacatedra': HoraCatedra.objects.get(id = horacatedra_id),
             'liquidarpago': LiquidarPago.objects.filter(hora_catedra = horacatedra_id),} 
    return redireccionar('admin/liquidar_pago.html', solicitud, datos)


@login_required
def reporteLiquidarPago(solicitud, horacatedra_id):
    resp = HttpResponse(mimetype='application/pdf')
    
#    tmp_estadoCuenta = MatriculaFinanciera.objects.filter(id=matriculafinanciera_id)
#    if tmp_estadoCuenta:
#        reporte = rpt_EstadoCuenta(queryset=tmp_estadoCuenta)
#        reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")
#        return resp
#    else:
#        solicitud.user.message_set.create(message="No existe datos para mostrar.")
#        return HttpResponseRedirect("/admin/financiero/matriculafinanciera")