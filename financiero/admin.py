# -*- coding: utf-8 -*-
from financiero.models import Pago, Letra, MatriculaFinanciera, Multa, HoraCatedra, CostoPrograma
from django.contrib import admin


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
  
  
class LetraInline(admin.TabularInline):
    model = Letra
    extra = 1
  
  
class MatriculaFinancieraAdmin(admin.ModelAdmin):
    raw_id_fields = ('matricula_ciclo',)
    
    fieldsets = [
        (None,  {'fields': [    'fecha_expedicion',
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
  
  
class MultaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': [  'fecha_expedicion',
                              'matricula_financiera',
                              'valor',
                              'concepto',
                              'fecha_pago',
                              'cancelada']}),
        ]
  
  
class HoraCatedraAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': [    'profesor',
                                'curso',
                                'valor_hora',
                                'observaciones']}),
    ]

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

admin.site.register(HoraCatedra, HoraCatedraAdmin)
admin.site.register(MatriculaFinanciera, MatriculaFinancieraAdmin)
admin.site.register(Multa, MultaAdmin)
admin.site.register(CostoPrograma, CostoProgramaAdmin)