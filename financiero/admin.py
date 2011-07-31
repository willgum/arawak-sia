# -*- coding: utf-8 -*-
from financiero.models import Pago, MatriculaFinanciera, HoraCatedra, CostoPrograma, Sesion, Adelanto, Descuento, CalendarioPago, Plazo
from django.contrib import admin
from academico.admin import ButtonableModelAdmin 

class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1

class PlazoInline(admin.TabularInline):
    model = Plazo
    extra = 1

class CalendarioPagoAdmin(admin.ModelAdmin):
    raw_id_fields = ('ciclo',)
    
    fieldsets = [
        (None,  {'fields': [    'ciclo', 
                                'programa'                                
                            ]}),
    ]
    filter_horizontal = ('programa',)
    inlines = [PlazoInline]
    
    list_display = (
        'ciclo',
        'programas',
        'plazos'
    )
    list_filter = ['ciclo', ]
    


  
class MatriculaFinancieraAdmin(admin.ModelAdmin):
    raw_id_fields = ('matricula_ciclo', 'calendario_pago',)
    readonly_fields = ('nombre_estudiante',
                       'valor_abonado',
                       'valor_matricula', 
                       'cursos_inscritos',
                       'saldo')
    
    fieldsets = [
        ('Resumen',  {'fields': [
                                'nombre_estudiante',    
                                'valor_matricula',
                                'valor_abonado',
                                'saldo',
                                'cursos_inscritos',]}),
        ('Información básica',  {'fields': [                              
                                'fecha_matricula',                                
                                'matricula_ciclo',
                                'calendario_pago',
                                'valor_inscripcion',                                
                                'descuento',                                
                                'paz_y_salvo']}),
    ]
    
    list_display = (
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'cursos_inscritos',
        'saldo',
        'paz_y_salvo',
    )
    
#    def reportecartera(self, request, obj):
#        obj.reporteCartera()
#    reportecartera.url = "/admin/financiero/matriculafinanciera/reportecartera"
#    reportecartera.short_description='Reporte cartera'
#    
#    def estadocuenta(self, request, obj):
#        obj.estadoCuenta()
#    estadocuenta.url = "/admin/financiero/matriculafinanciera/estadocuenta"
#    estadocuenta.short_description='Estado de cuenta'
    
    
    inlines = [PagoInline, ]
#    buttons_list = [reportecartera, ]
#    buttons = [estadocuenta, ]
    
    list_filter = ['paz_y_salvo', ]
    search_fields = ('inscripcion_programa__matricula_programa__estudiante__nombre1',
                     'inscripcion_programa__matricula_programa__estudiante__nombre2',
                     'inscripcion_programa__matricula_programa__estudiante__apellido1',
                     'inscripcion_programa__matricula_programa__estudiante__apellido1',
                     'inscripcion_programa__matricula_programa__codigo',)
    date_hierarchy = 'fecha_matricula'
  
  
class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1
    raw_id_fields = ('curso', )
    
    
class AdelantoInLine(admin.TabularInline):
    model = Adelanto
    extra = 1


class DescuentoInLine(admin.TabularInline):
    model = Descuento
    extra = 1


class HoraCatedraAdmin(ButtonableModelAdmin):
    raw_id_fields = ('profesor', 'ciclo')
    
    fieldsets = [
        ('Información básica', {'fields': [    
                                'profesor',
                                'ciclo',
                                'tiempo_hora',
                                'valor_hora',
                                'observaciones']}),
    ]
    
    list_display = (
            'profesor',
            'ciclo',
            'tiempo_hora',
            'valor_hora'
                    )
    
#    def liquidarpago(self, request, obj):
#        obj.liquidarpago()
#    liquidarpago.url = "/admin/financiero/horacatedra/liquidarpago"
#    liquidarpago.short_description='Liquidar pago'
    
#    def liquidarnomina(self, request, obj):
#        obj.estadoCuenta()
#    liquidarnomina.url = "/admin/financiero/horacatedra/liquidarnomina"
#    liquidarnomina.short_description='Reporte nómina'
    
    
    inlines = [AdelantoInLine, DescuentoInLine, SesionInline, ]
#    buttons = [liquidarpago, ] 
#    buttons_list = [liquidarnomina, ]
    

class CostoProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': [    'ciclo',
                                'programa',
                                'valor',
                                'valor_credito']}),
    ]
    filter_horizontal = ('programa',)
    raw_id_fields = ('ciclo',)
    
    list_display = (
        'ciclo',
        'programas',
        'valor',
        'valor_credito'
    )

    list_filter = ['ciclo',]
    

admin.site.register(CostoPrograma, CostoProgramaAdmin)
admin.site.register(CalendarioPago, CalendarioPagoAdmin)
admin.site.register(HoraCatedra, HoraCatedraAdmin)
admin.site.register(MatriculaFinanciera, MatriculaFinancieraAdmin)


