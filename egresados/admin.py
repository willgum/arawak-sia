# -*- coding: utf-8 -*-
from egresados.models import HojaVida, Egresado, Oferta, Empresa, OtrosEstudiosEgresado
from django.contrib import admin

class OfertaInline(admin.TabularInline):
    model = Oferta
    extra = 1
    raw_id_fields = ('empresa',)
    fields = ('titulo', 'fecha_publicacion', 'fecha_cierre')

class EmpresaAdmin(admin.ModelAdmin):
    fieldsets = [
         (None, {'fields': [
            'nombre', 
            'descripcion',
            'direccion',
            'ciudad',
            'pais',
            'telefono',
            'fax',
            'email',
            'web',]}),
    ]
    
    list_display = (
        'nombre', 
        'ciudad', 
        'pais', 
        'email',
        'web',
    )
    inlines = [OfertaInline]
    list_filter = ['ciudad', 'pais']
    search_fields = ('nombre','ciudad')
    
class OfertaAdmin(admin.ModelAdmin):
    fieldsets = [
         (None, {
            'fields': [
                'empresa', 
                'codigo',
                'titulo',
                'descripcion',
                'requisitos',
                'nivel_cargo',
                'sector',
                'salario',
                'ciudad',
                'pais',
                'fecha_publicacion',
                'fecha_cierre'
                ]
            }
         ),
    ]
    
    list_display = (
        'codigo',
        'titulo', 
        'empresa', 
        'ciudad', 
        'pais',
        'vigente',       
    )
    
    list_filter = ['empresa', 'ciudad', 'pais', 'salario',]
    search_fields = ('titulo', 'titulo', 'empresa',)
    
    
class HojaVidaInline(admin.TabularInline):
    model = HojaVida
    extra = 1
    
class OtrosEstudiosEgresadoInline(admin.TabularInline):
    model = OtrosEstudiosEgresado
    extra = 1

class EgresadoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion Personal', {'fields': [ 
            'nombre', 
            'apellido', 
            'sexo', 
            'tipo_documento', 
            'documento', 
            'lugar_expedicion',
            'fecha_nacimiento', 
            'lugar_nacimiento'], 
            'classes': ['collapse']}),
        ('Informacion de contacto', {'fields': [
            'direccion', 
            'lugar_residencia', 
            'telefono', 
            'email', 
            'web'], 
            'classes': ['collapse']}),
        ('Informacion de acceso', {'fields': [
            'usuario', 
            'contrasena'], 
            'classes': ['collapse']}),
    ]
    inlines = [OtrosEstudiosEgresadoInline, HojaVidaInline]
    list_display = ('documento', 'nombre', 'apellido', 'email',)
    search_fields = ('documento', 'nombre', 'apellido',)


admin.site.register(Egresado, EgresadoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Oferta, OfertaAdmin)