# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid
from django.views.static import HttpResponseRedirect                                                        # se incorporo para poder acceder a archivos estaticos
#Reportes GERALDO
from reportes import rpt_ReporteCartera, rpt_EstadoCuenta

from geraldo.generators import PDFGenerator


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