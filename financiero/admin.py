# -*- coding: utf-8 -*-
from financiero.models import Pago, Letra, MatriculaFinanciera, HoraCatedra, CostoPrograma, Sesion, InscripcionPrograma
from django.contrib import admin


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

  
class MatriculaFinancieraAdmin(admin.ModelAdmin):
    raw_id_fields = ('inscripcion_programa', 'matricula_ciclo',)
    
    fieldsets = [
        (None,  {'fields': [    'inscripcion_programa',
                                'fecha_expedicion',
                                'matricula_ciclo', 
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
        'inscripcion_ciclo',
        'paz_y_salvo'
    )
    
    inlines = [LetraInline, PagoInline]
    
    list_filter = ['paz_y_salvo', 'matricula_ciclo',]
    search_fields = ('codigo_estudiante', 'inscripcion_ciclo')
    date_hierarchy = 'fecha_expedicion'
    readonly_fields = ('valor_abonado','valor_matricula')
  
  
class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1
    raw_id_fields = ('curso', )
  
class HoraCatedraAdmin(admin.ModelAdmin):
    raw_id_fields = ('profesor', 'ciclo')
    
    fieldsets = [
        (None,  {'fields': [    'profesor',
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
