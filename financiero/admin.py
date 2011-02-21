# -*- coding: utf-8 -*-
from financiero.models import Pago, Letra, MatriculaFinanciera, HoraCatedra, CostoPrograma, Sesion, InscripcionPrograma
from django.contrib import admin
from academico.admin import ButtonableModelAdmin 

class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
  
  
class LetraInline(admin.TabularInline):
    model = Letra
    extra = 1
  
  
class InscripcionProgramaAdmin(admin.ModelAdmin):
    raw_id_fields = ('matricula_programa',)
    
    fieldsets = [
        (None,  {'fields': [    'fecha_inscripcion',
                                'matricula_programa', 
                                'valor_inscripcion',
                                'fecha_pago'
                            ]}),
    ]
    
    list_display = (
        'fecha_inscripcion',
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'valor_inscripcion',
        'fecha_pago'
    )
    
    search_fields = ('matricula_programa', )
    date_hierarchy = 'fecha_inscripcion'

  
class MatriculaFinancieraAdmin(ButtonableModelAdmin):
    raw_id_fields = ('inscripcion_programa', 'ciclo',)
    
    fieldsets = [
        ('Información básica',  {'fields': [    
                                'inscripcion_programa',
                                'fecha_expedicion',
                                'ciclo', 
                                'becado',
                                'valor_descuento',
                                'valor_matricula',
                                'valor_abonado',
                                'paz_y_salvo',
                                'cuotas']}),
    ]
    
    list_display = (
        'fecha_expedicion',
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'ciclo',
        'paz_y_salvo'
    )
    
    def reporteCartera(self, request, obj):
        obj.reporteCartera()
    reporteCartera.url = "/admin/financiero/matriculafinanciera/reportecartera"
    reporteCartera.short_description='Reporte cartera'
    
    def estadoCuenta(self, request, obj):
        obj.estadoCuenta()
    estadoCuenta.url = "/admin/financiero/matriculafinanciera/estadoCuenta"
    estadoCuenta.short_description='Estado de cuenta'
    
    
    inlines = [LetraInline, PagoInline]
    buttons_list = [reporteCartera, ]
    buttons = [estadoCuenta, ]
    
    list_filter = ['paz_y_salvo', 'ciclo',]
    search_fields = ('inscripcion_programa__matricula_programa__estudiante__nombre1',
                     'inscripcion_programa__matricula_programa__estudiante__nombre2',
                     'inscripcion_programa__matricula_programa__estudiante__apellido1',
                     'inscripcion_programa__matricula_programa__estudiante__apellido1',
                     'inscripcion_programa__matricula_programa__codigo', 'ciclo__codigo')
    date_hierarchy = 'fecha_expedicion'
    readonly_fields = ('valor_abonado','valor_matricula')
  
  
class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1
    raw_id_fields = ('curso', )
  
class HoraCatedraAdmin(admin.ModelAdmin):
    raw_id_fields = ('profesor', 'ciclo')
    
    fieldsets = [
        ('Información básica', {'fields': [    
                                'profesor',
                                'ciclo',
                                'valor_hora',
                                'observaciones']}),
    ]
    
    inlines = [SesionInline, ] 

class CostoProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': [    'programa',
                                'ciclo',
                                'valor']}),
    ]
    
    list_display = (
        'nombre_programa',
        'codigo_ciclo',
        'valor'
    )
    
    list_filter = ['ciclo',]
    search_fields = ('nombre_programa', 'codigo_ciclo')
    raw_id_fields = ('programa', 'ciclo')

admin.site.register(InscripcionPrograma, InscripcionProgramaAdmin)
admin.site.register(MatriculaFinanciera, MatriculaFinancieraAdmin)
admin.site.register(CostoPrograma, CostoProgramaAdmin)
admin.site.register(HoraCatedra, HoraCatedraAdmin)
