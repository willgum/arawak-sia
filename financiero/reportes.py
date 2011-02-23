# -*- coding: utf-8 -*-
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings
from datetime import date

from geraldo import Report, ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label, FIELD_ACTION_SUM, SubReport, Image, ReportGroup

import Image as PILImage
import os

from reportlab.lib.pagesizes import LETTER, portrait, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY, TA_LEFT


cur_dir = settings.MEDIA_ROOT

meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
def get_encabezado(graphic):
    filename = os.path.join(cur_dir, 'imagenes/original/encabezado.jpg')
    if os.path.exists(filename):
        return PILImage.open(filename)
    else:
        return None

class PageFooterBand(ReportBand):
        height = 0*cm
        elements = [
                Label(text='http://arawak.com.co', width=BAND_WIDTH, style={'fontSize':8, 'alignment': TA_CENTER}),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'fontSize':8, 'alignment': TA_LEFT}),
                SystemField(expression=u'Impreso %(now:%b %d, %Y)s %(now:%H:%M)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'fontSize':8, 'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}

class PageHeaderBand(ReportBand):
        height = 1.8*cm
        elements = [
                Image(left=0*cm, top=0*cm, get_image=get_encabezado),
                Label(text="INSTITUTO EDUCATIVO DE PRUEBA", top=0*cm, left=0, width=BAND_WIDTH,
                      style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
                SystemField(expression='%(report_title)s', top=0.8*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 13, 'alignment': TA_CENTER}),
                ]
        borders = {'bottom': True}
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
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
        
    class band_begin(ReportBand):
        height = 0.9*cm
        elements = [
                Label(text="Estudiante", top=0.4*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Programa", top=0.4*cm, left=5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Ciclo", top=0.4*cm, left=10*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. matrícula", top=0.4*cm, left=11.5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. abonado", top=0.4*cm, left=14*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Vlr. Saldo", top=0.4*cm, left=16.5*cm, style={'fontName': 'Helvetica-Bold'}),
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
        
#===============================================================================
# CLASE PARA IMPRIMIR CUENTA DE ESTUDIANTE 
#===============================================================================

class rpt_EstadoCuenta(Report):
    title = 'Estado de cuenta de estudiante'
    author = 'Arawak-Claro'
    
    page_size = LETTER
    margin_left = 1.5*cm
    margin_top = 1.6*cm
    margin_right = 1.5*cm
    margin_bottom = 1*cm
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
    
    class band_begin(ReportBand):
        height = 0.1*cm

    class band_detail(ReportBand):
        auto_expand_height = True
        
        elements=(
            Label(text="Estudiante:", top=0*cm, left=0, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'nombre_estudiante', top=0*cm, left=2*cm),
            Label(text="Programa:", top=0.5*cm, left=0, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'nombre_programa', top=0.5*cm, left=2*cm),
            )
        
    subreports = [
        SubReport(
#                  Message.objects.filter(user__id=%(object)s.id)'
#            queryset_string = '%(object)s.objects.filter(id=%(object)s.id)',
            band_header = ReportBand(
                height=0.5*cm,
                elements=[
                     Label(text='Fecha expedición', top=0, left=0.2*cm, style={'fontName': 'Helvetica-Bold'}),
                     Label(text='Valor', top=0, left=4*cm, style={'fontName': 'Helvetica-Bold'}),
                ],
                borders={'top': True, 'left': True, 'right': True},
            ),
            band_detail = ReportBand(
                height=0.5*cm,
                elements=[
                    ObjectValue(attribute_name='fecha_expedicion', top=0, left=0.2*cm),
                    ObjectValue(attribute_name='valor', top=0, left=4*cm),
                 ],
                 borders={'left': True, 'right': True},
            ),
        ),
    ]
    
    class band_summary(ReportBand):
        height = 1*cm
        elements = [
            Label(text="Valores totales", top=0.1*cm, left=0, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name='valor_matricula', top=0.1*cm, left=8.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_abonado', top=0.1*cm, left=11*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_saldo', top=0.1*cm, left=13.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}
        
        
#===============================================================================
# CLASE PARA IMPRIMIR LIQUIDACIÓN DE PAGO A DOCENTE 
#===============================================================================

class rpt_LiquidarPagoDocente(Report):
    title = 'Liquidación de pago a docente'
    author = 'Arawak-Claro'
    
    page_size = LETTER
    margin_left = 1.5*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
    
    class band_begin(ReportBand):
        height = 0.1*cm
        
    class band_detail(ReportBand):
        auto_expand_height = True
        
        elements=(
            Label(text="Recibo No.:", top=0*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'recibo', top=0*cm, left=3*cm),
            Label(text="Fecha:", top=0.5*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'fecha_liquidacion', left=3*cm, top=0.5*cm, 
                        get_value=lambda instance: str(instance.fecha_liquidacion.day) + ' de ' + meses[instance.fecha_liquidacion.month] + ' de ' + str(instance.fecha_liquidacion.year)),
            Label(text="Total:", top=0.5*cm, left=14*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'valor_total', top=0.5*cm, left=12.5*cm, style={'alignment': TA_RIGHT}),
            Label(text="Pagado a:", top=1*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'hora_catedra.profesor.nombre', top=1*cm, left=3*cm),
            Label(text="Por concepto de:", top=1.5*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name = u'fecha_liquidacion', left=3*cm, top=1.5*cm, width=16*cm, 
                        get_value=lambda instance: u'Pago correspondiente a las horas cátedra dictadas del ' +
                        str(instance.fecha_inicio.day) + ' de ' + meses[instance.fecha_inicio.month] + ' de ' + str(instance.fecha_inicio.year) + ' al ' +\
                        str(instance.fecha_fin.day) + ' de ' + meses[instance.fecha_fin.month] + ' de ' + str(instance.fecha_fin.year) + '.'),
            Label(text="Valor liquidado:", top=2.5*cm, left=0*cm),
            ObjectValue(attribute_name='valor_liquidado', top=2.5*cm, left=0*cm, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            Label(text="Valor adelantos:", top=3*cm, left=0*cm),
            ObjectValue(attribute_name='valor_adelanto', top=3*cm, left=0*cm, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            Label(text="Valor descuentos:", top=3.5*cm, left=0*cm),
            ObjectValue(attribute_name='valor_descuento', top=3.5*cm, left=0*cm, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            Label(text="Total:", top=4*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name='valor_total', top=4*cm, left=0*cm, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            )
    
    groups = [
        ReportGroup(attribute_name='recibo',
            band_header=ReportBand(
                height=0.4*cm,
            ),
            band_footer=ReportBand(
                height=0.3*cm,
                borders={'bottom': True},
            ),
        ),
    ]
#    class band_summary(ReportBand):
#        height = 1*cm
#        borders = {'top': True}
        
        
#===============================================================================
# CLASE PARA IMPRIMIR LIQUIDACIÓN DE NÓMINA DE DOCENTES 
#===============================================================================

class rpt_LiquidarNominaDocente(Report):
    title = 'Reporte de liquidación de pago a docente'
    author = 'Arawak-Claro'
    
    page_size = LETTER
    margin_left = 1.5*cm
    margin_top = 1.6*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
    
    class band_begin(ReportBand):
        height = 0.9*cm
        elements = [
                Label(text="Recibo", top=0.4*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Profesor", top=0.4*cm, left=1.5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Fecha pago", top=0.4*cm, left=7*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Subtotal", top=0.4*cm, left=9.5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Adelantos", top=0.4*cm, left=12*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Descuentos", top=0.4*cm, left=14.5*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text="Total", top=0.4*cm, left=17*cm, style={'fontName': 'Helvetica-Bold'}),
                ]
        borders = {'bottom': True}
        
    class band_detail(ReportBand):
        auto_expand_height = True
        
        elements=(
            ObjectValue(attribute_name = u'recibo', top=0.1*cm, left=0*cm),
            ObjectValue(attribute_name = u'hora_catedra.profesor.nombre', top=0.1*cm, left=1.5*cm),
            ObjectValue(attribute_name = u'fecha_liquidacion', top=0.1*cm, left=7*cm),
            ObjectValue(attribute_name = u'valor_liquidado', top=0.1*cm, left=6*cm, style={'alignment': TA_RIGHT}),
            ObjectValue(attribute_name = u'valor_adelanto', top=0.1*cm, left=8.5*cm, style={'alignment': TA_RIGHT}),
            ObjectValue(attribute_name = u'valor_descuento', top=0.1*cm, left=11*cm, style={'alignment': TA_RIGHT}),
            ObjectValue(attribute_name = u'valor_total', top=0.1*cm, left=13.5*cm, style={'alignment': TA_RIGHT}),
            )
        
    class band_summary(ReportBand):
        height = 1*cm
        elements = [
            Label(text="Valores totales", top=0.1*cm, left=0, style={'fontName': 'Helvetica-Bold'}),
            ObjectValue(attribute_name='valor_liquidado', top=0.1*cm, left=6*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_adelanto', top=0.1*cm, left=8.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_descuento', top=0.1*cm, left=11*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
            ObjectValue(attribute_name='valor_total', top=0.1*cm, left=13.5*cm, action=FIELD_ACTION_SUM, style={'fontName': 'Helvetica-Bold', 'alignment': TA_RIGHT}),
        ]