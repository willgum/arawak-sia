# -*- coding: utf-8 -*-
from datetime import date
import Image as PILImage
import os
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings

from geraldo import Report, ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label, Image, ReportGroup, FIELD_ACTION_SUM

from reportlab.lib.pagesizes import LETTER, portrait, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY

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
# CLASE PARA IMPRIMIR REPORTE CARNÉ DE ESTUDIANTES 
#===============================================================================

def get_foto_usuario(graphic):
    filename = os.path.join(cur_dir,'%s'%str(graphic.instance.estudiante.foto).replace('original','thumbnail'))
    if len('%s'%str(graphic.instance.estudiante.foto)) > 0:
        if os.path.exists(filename):
            return PILImage.open(filename)
        else:
            return None
    else:
        return None
    
class rpt_EstudianteCarnet(Report):
    title = 'Consolidado de estudiantes inscritos por programa'
    author = 'Arawak-Claro'
    
    personal = (8.5*cm, 5.5*cm)
    page_size = landscape(personal)
    margin_left = 0.1*cm
    margin_top = 0.1*cm
    margin_right = 0.1*cm
    margin_bottom = 0.1*cm
    
    class band_begin(ReportBand):
        height = 1*cm
        elements=(
            Image(left=3*cm, top=0*cm, get_image=get_encabezado),
                  )
         
    class band_detail(ReportBand):
        auto_expand_height = True
        
        elements=(
            Image(left=0.3*cm, top=0*cm, get_image=get_foto_usuario),
            Label(text='Nombre', left=3*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 9}),
            ObjectValue(attribute_name = u'estudiante.nombre', top=0.4*cm, left=3*cm),
            Label(text='Identificación', left=3*cm, top=1*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 9}),
            ObjectValue(attribute_name = u'estudiante.documento', top=1.4*cm, left=3*cm),
            Label(text='RH', left=6*cm, top=1*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 9}),
            ObjectValue(attribute_name = u'estudiante.grupo_sanguineo.nombre', top=1.4*cm, left=6*cm, width=BAND_WIDTH),
            Label(text='Código', left=3*cm, top=2*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 9}),
            ObjectValue(attribute_name = u'codigo', top=2.4*cm, left=3*cm, width=BAND_WIDTH),
            Label(text='Programa', left=3*cm, top=3*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 9}),
            ObjectValue(attribute_name = u'programa.nombre', top=3.4*cm, left=3*cm, width=BAND_WIDTH),
            )
        
    class band_page_footer(ReportBand):
        height = 0.3*cm
        elements = [
                Label(text='http://arawak.com.co', width=BAND_WIDTH, style={'fontSize':8, 'alignment': TA_CENTER}),
                ]
        borders = {'top': True}
       
                
#===============================================================================
# CLASE PARA IMPRIMIR CONSTANCIA DE ESTUDIO DE ESTUDIANTES 
#===============================================================================
class rpt_ConstanciaCiclo(Report):
    title = 'Listado de ciclos'
    author = 'Arawak-Claro'
    
    page_size = LETTER
    margin_left = 2.5*cm
    margin_top = 3*cm
    margin_right = 2*cm
    margin_bottom = 1*cm
    band_page_footer = PageFooterBand
    
    class band_detail(ReportBand):
        height = 0.5*cm
        
        
#        TODO: El caso ideal es diseñar el texto de la constancia en un archivo de texto independiente, para que funcione de manera más dinámica.
        elements = [
                    ObjectValue(left=0, attribute_name= u'observaciones', top=1*cm, width=16*cm,
                        get_value=lambda instance: u'Que el(la) estudiante ' +\
                            instance.matricula_programa.estudiante.nombre() +\
                            ' identificado(a) con ' + instance.matricula_programa.estudiante.tipo_documento.nombre +\
                            u' número ' + instance.matricula_programa.estudiante.documento + ' de ' +\
                            instance.matricula_programa.estudiante.lugar_expedicion +\
                            ', se encuentra ' + instance.matricula_programa.estado.nombre + ' en el programa ' +\
                            instance.matricula_programa.programa.nombre + u' de esta Institución Educativa para el periodo comprendido del ' +\
                            str(instance.ciclo.fecha_inicio) + ' hasta el ' + str(instance.ciclo.fecha_fin) + '.<br/><br/>' +\
                            u'Se expide por solicitud del interesado para trámites personales, el día ' +\
                            str(date.today().day) + ' de ' + meses[date.today().month] + u' de ' + str(date.today().year) + '.',   
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

#===============================================================================
# CLASE PARA IMPRIMIR LISTADO DE ESTUDIANTES INSCRITOS CON LOS DISTINTOS ESTADOS 
#===============================================================================
class rpt_EstudiantesInscritos(Report):
    title = 'Listado de estudiantes inscritos'
    author = 'Edwar Carranza'
    
    page_size = landscape(LETTER)
    margin_left = 2*cm
    margin_top = 1.5*cm
    margin_right = 1.5*cm
    margin_bottom = 1.5*cm
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
    
    class band_begin(ReportBand):
        height = 0.9*cm
       
    class band_detail(ReportBand):
        auto_expand_height = True
        margin_bottom = 0.1*cm
        
        elements=(
            ObjectValue(left=0*cm, top=0.1*cm, width=10*cm, attribute_name=u'estudiante.nombre'),
            ObjectValue(left=11.2*cm, top=0.1*cm, attribute_name=u'estado.nombre'),
            ObjectValue(left=13.7*cm, top=0.1*cm, attribute_name=u'estudiante.email'),
            ObjectValue(left=18.7*cm, top=0.1*cm, attribute_name=u'estudiante.telefono'),
            ObjectValue(left=22*cm, top=0.1*cm, attribute_name=u'estudiante.movil'),
            )
    
    groups = [
        ReportGroup(attribute_name='programa',
            band_header=ReportBand(
                height = 1.3*cm,
                elements=[
                          Label(text="Programa:", top=0*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                          ObjectValue(left=2.3*cm, top=0*cm, width=10*cm, attribute_name = u'programa.nombre', style={'fontName': 'Helvetica-Bold'}),
                          
                          Label(text="Estudiante", top=0.7*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                          Label(text=u"Estado", top=0.7*cm, left=11.2*cm, style={'fontName': 'Helvetica-Bold'}),
                          Label(text=u"email", top=0.7*cm, left=13.7*cm, style={'fontName': 'Helvetica-Bold'}),
                          Label(text=u"Telefono", top=0.7*cm, left=18.7*cm, style={'fontName': 'Helvetica-Bold'}),
                          Label(text=u"Móvil", top=0.7*cm, left=22*cm, style={'fontName': 'Helvetica-Bold'}),
                          ],
                borders = {'bottom': True}
            ),
            
            band_footer=ReportBand(
                height=0.7*cm,
                borders = {'top': True}
            ),
        ),   
    ]
        
        

#===============================================================================
# CLASE PARA IMPRIMIR CONSOLIDADO DE ESTUDIANTES INSCRITOS 
#===============================================================================
class rpt_ConsolidadoInscritos(Report):
    title = 'Consolidado de estudiantes inscritos por programa'
    author = 'Arawak-Claro'
    
    page_size = landscape(LETTER)
    margin_left = 2*cm
    margin_top = 1.5*cm
    margin_right = 1.5*cm
    margin_bottom = 1.5*cm
    band_page_footer = PageFooterBand
    band_page_header = PageHeaderBand
    
    class band_begin(ReportBand):
        height = 0.9*cm
        elements = [
                Label(text="Programa", top=0.3*cm, left=0*cm, style={'fontName': 'Helvetica-Bold'}),
                Label(text=u"Activos", top=0.3*cm, left=7.5*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                Label(text=u"Egresados", top=0.3*cm, left=10*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                Label(text=u"Pendientes", top=0.3*cm, left=12.5*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                Label(text=u"Expulsados", top=0.3*cm, left=15*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                Label(text=u"Retirados", top=0.3*cm, left=17.5*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                Label(text=u"Suspendidos", top=0.3*cm, left=20*cm, style={'fontName': 'Helvetica-Bold', 'alignment':TA_CENTER}),
                ]
        borders = {'bottom': True}
         
    class band_detail(ReportBand):
        auto_expand_height = True
        margin_bottom = 0.1*cm
        
    groups = [
        ReportGroup(attribute_name='programa',
            band_header=ReportBand(
                auto_expand_height = True,
                elements=[
                          ObjectValue(left=0*cm, top=0*cm, width=10*cm, attribute_name = u'programa.nombre'),
                          ObjectValue(left=5*cm, top=0*cm, attribute_name=u'estudianteActivo', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ObjectValue(left=7.5*cm, top=0*cm, attribute_name=u'estudianteEgresado', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ObjectValue(left=10*cm, top=0*cm, attribute_name=u'estudiantePendiente', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ObjectValue(left=12.5*cm, top=0*cm, attribute_name=u'estudianteExpulsado', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ObjectValue(left=15*cm, top=0*cm, attribute_name=u'estudianteRetirado', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ObjectValue(left=17.5*cm, top=0*cm, attribute_name=u'estudianteSuspendido', action=FIELD_ACTION_SUM, style={'alignment': TA_RIGHT}),
                          ]
            ),
        ),
    ]
        