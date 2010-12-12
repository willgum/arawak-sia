# -*- coding: utf-8 -*-
from financiero.models import *
from django.contrib import admin


class PagoInline(admin.TabularInline):
  model = Pago
  extra = 1
  
  
class LetraInline(admin.TabularInline):
  model = Letra
  extra = 1
  
  
class MatriculaFinancieraAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,  {'fields': [
              'fecha_expedicion',
              'inscripcion_estudiante', 
              'estado',
              'becado',
              'valor_inscripcion',
              'valor_matricula',
              'cuotas',
              'cancelada']}),
  ]
  inlines = [PagoInline, LetraInline]
  
  
class MultaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,  {'fields': [
              'fecha_expedicion',
              'matricula_financiera',
              'valor',
              'concepto',
              'fecha_pago',
              'cancelada']}),
  ]
  
  
admin.site.register(Multa, MultaAdmin)
admin.site.register(MatriculaFinanciera, MatriculaFinancieraAdmin)
