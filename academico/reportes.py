# -*- coding: utf-8 -*-
import datetime

from geraldo import Report, landscape, ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY

class rpt_Ciclo(Report):
    title = 'Listado de ciclos'
    author = 'Edwar Carranza'
    
    page_size = landscape(LETTER)
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm

    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='id', left=0.5*cm),
            ObjectValue(attribute_name='codigo', left=3*cm),
            ObjectValue(attribute_name='fecha_inicio', left=6*cm,
                get_value=lambda instance: instance.fecha_inicio.strftime('%m/%d/%Y')),
            )
        
    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
                Label(text="ID", top=0.8*cm, left=0.5*cm),
                Label(text=u"Codigo", top=0.8*cm, left=3*cm),
                Label(text=u"Fecha inicio", top=0.8*cm, left=6*cm),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
#        borders = {'bottom': True, 'top': True}
    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='Geraldo Reports', top=0.1*cm),
                SystemField(expression=u'Printed in %(now:%Y, %b %d)s at %(now:%H:%M)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}
        
        
class rpt_ConstanciaCiclo(Report):
    title = 'Listado de ciclos'
    author = 'Edwar Carranza'
    
    page_size = LETTER
    margin_left = 2.5*cm
    margin_top = 3*cm
    margin_right = 2*cm
    margin_bottom = 1*cm
    meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    class band_detail(ReportBand):
        height = 0.5*cm
        
        
#        TODO: El caso ideal es diseñar el texto de la constancia en un archivo de texto independiente, para que funcione de manera más dinámica.
        elements = [
                    ObjectValue(left=0, top=1*cm, width=16*cm,
                        get_value=lambda instance: u'Que el(la) estudiante ' +\
                            instance.matricula_programa.estudiante.nombre() +\
                            ' identificado(a) con ' + instance.matricula_programa.estudiante.tipo_documento.nombre +\
                            u' número ' + instance.matricula_programa.estudiante.documento + ' de ' +\
                            instance.matricula_programa.estudiante.lugar_expedicion +\
                            ', se encuentra ' + instance.matricula_programa.estado.nombre + ' en el programa ' +\
                            instance.matricula_programa.programa.nombre + u' de esta Institución Educativa para el periodo comprendido del ' +\
                            str(instance.ciclo.fecha_inicio) + ' hasta el ' + str(instance.ciclo.fecha_fin) + '.<br/><br/>' +\
                            u'Se expide por solicitud del interesado para trámites personales, el día ' +\
                            str(datetime.date.today().day) + ' de ' + rpt_ConstanciaCiclo.meses[datetime.date.today().month] + u' de ' + str(datetime.date.today().year) + '.',   
                        style={'alignment': TA_JUSTIFY, 'fontSize': 11})
        ]
        
    class band_page_header(ReportBand):
        height = 1.3*cm
        auto_expand_height = True
        elements = [
                Label(text='El suscrito director', top=0.1*cm, width=BAND_WIDTH, 
                      style={'alignment': TA_CENTER, 'fontName': 'Helvetica-Bold', 
                             'fontSize': 13}),
                Label(text='Hace constar:', top=1*cm, width=BAND_WIDTH, 
                      style={'alignment': TA_CENTER, 'fontName': 'Helvetica-Bold', 'fontSize': 13}),
                
                ]
    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='http://arawak.com.co', top=0.1*cm),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_CENTER}),
                SystemField(expression=u'Impreso %(now:%b %d, %Y)s %(now:%H:%M)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}
        
        
class rpt_EstudiantesInscritos(Report):
    title = 'Listado de estudiantes inscritos'
    author = 'Edwar Carranza'
    
    page_size = landscape(LETTER)
    margin_left = 2*cm
    margin_top = 1.5*cm
    margin_right = 1.5*cm
    margin_bottom = 1.5*cm
    
    class band_begin(ReportBand):
        height = 1*cm
         
    class band_detail(ReportBand):
        auto_expand_height = True
        
        margin_bottom = 0.1*cm
        
        elements=(
            ObjectValue(left=0.2*cm, top=0.1*cm, get_value=lambda instance: instance.estudiante.nombre()),
            ObjectValue(left=6*cm, top=0.1*cm, get_value=lambda instance: instance.programa.nombre),
            ObjectValue(left=11.2*cm, top=0.1*cm, get_value=lambda instance: instance.estado.nombre),
            ObjectValue(left=13.7*cm, top=0.1*cm, get_value=lambda instance: instance.estudiante.email),
            ObjectValue(left=18.7*cm, top=0.1*cm, get_value=lambda instance: instance.estudiante.telefono),
            ObjectValue(left=22*cm, top=0.1*cm, get_value=lambda instance: instance.estudiante.movil),
            )
        
    class band_page_header(ReportBand):
        height = 1.6*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
                Label(text="Estudiante", top=1.1*cm, left=0.2*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Programa", top=1.1*cm, left=6*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Estado", top=1.1*cm, left=11.2*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"email", top=1.1*cm, left=13.7*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Telefono", top=1.1*cm, left=18.7*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Móvil", top=1.1*cm, left=22*cm, style={'fontName': 'Helvetica-Bold'}),
                ]
        borders = {'bottom': True}
    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='http://arawak.com.co', top=0.1*cm),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_CENTER}),
                SystemField(expression=u'Impreso %(now:%b %d, %Y)s %(now:%H:%M)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}