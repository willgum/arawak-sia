# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from financiero.models import MatriculaFinanciera
from django.contrib.auth.decorators import login_required                                                   # me permite usar eö @login_requerid

#Reportes GERALDO
from reportes import rpt_ReporteCartera
from geraldo.generators import PDFGenerator


@login_required
def reporteCartera(solicitud):
    resp = HttpResponse(mimetype='application/pdf')
    
    tmp_matriculafinanciera = MatriculaFinanciera.objects.filter(paz_y_salvo=False).order_by('inscripcion_programa__matricula_programa__programa')
    reporte = rpt_ReporteCartera(queryset=tmp_matriculafinanciera)
    reporte.generate_by(PDFGenerator, filename=resp, encode_to="utf-8")

    return resp