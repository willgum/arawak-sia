# -*- coding: utf-8 -*-
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings

from geraldo import Report, ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label, FIELD_ACTION_SUM

from reportlab.lib.pagesizes import LETTER, portrait, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY


cur_dir = settings.MEDIA_ROOT

#===============================================================================
# CLASE PARA IMPRIMIR REPORTE DE CARTERA 
#===============================================================================

class rpt_ReporteCartera(Report):
    title = 'Reporte de cartera de estudiantes'
    author = 'Arawak-Claro'
    
    page_size = LETTER
    margin_left = 1.5*cm
    margin_top = 1.6*cm
    margin_right = 1.5*cm
    margin_bottom = 1*cm
    
    class band_begin(ReportBand):
        height = 0.1*cm
        
    class band_page_header(ReportBand):
        height = 1.1*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
                Label(text="Estudiante", top=0.7*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Programa", top=0.7*cm, left=5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Ciclo", top=0.7*cm, left=10*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. matrícula", top=0.7*cm, left=11.5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. abonado", top=0.7*cm, left=14*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. Saldo", top=0.7*cm, left=16.5*cm, style={'fontName': 'Helvetica-Bold'}),
                ]
        borders = {'bottom': True}
         
    class band_detail(ReportBand):
        auto_expand_height = True
        
        elements=(
            ObjectValue(attribute_name = u'nombre_estudiante', top=0.1*cm, left=0*cm),
            ObjectValue(attribute_name = u'nombre_programa', top=0.1*cm, left=5*cm),
            ObjectValue(attribute_name = u'ciclo', top=0.1*cm, left=10*cm),
            ObjectValue(attribute_name = u'valor_matricula', top=0.1*cm, left=8.5*cm, style={'alignment': TA_RIGHT}),
            ObjectValue(attribute_name = u'valor_abonado', top=0.1*cm, left=11*cm, style={'alignment': TA_RIGHT}),
            ObjectValue(attribute_name = u'valor_saldo', top=0.1*cm, left=13.5*cm, style={'alignment': TA_RIGHT}),
            )
    
    class band_summary(ReportBand):
        height = 1*cm
        elements = [
            Label(text="Valores totales", top=0.1*cm, left=0, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name='valor_matricula', top=0.1*cm, left=8.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_abonado', top=0.1*cm, left=11*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_saldo', top=0.1*cm, left=13.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}
        
    class band_page_footer(ReportBand):
        height = 0*cm
        elements = [
                Label(text='http://arawak.com.co', width=BAND_WIDTH, style={'fontSize':8, 'alignment': TA_CENTER}),
                ]
        borders = {'top': True}