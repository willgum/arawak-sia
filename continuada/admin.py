# -*- coding: utf-8 -*-
from continuada.models import Curso, Estudiante, InscripcionCurso
from django.contrib import admin


class InscripcionCursoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'fecha_inscripcion',
            'curso', 
            'estudiante',
            'codigo',
            'fecha_vencimiento', 
            'nota']}),
    ]
    
    list_display = (
        'curso', 
        'estudiante', 
        'codigo',
        'fecha_inscripcion',
        'fecha_vencimiento',
        'nota',
    )
    search_fields = ['curso', 'estudiante']

class CursoAdmin(admin.ModelAdmin):
    fieldsets = [
         (None, {'fields': [ 
            'tipo_curso',
            'codigo', 
            'nombre', 
            'descripcion', 
            'intensidad', 
            'horario']}
         ),
    ]
    list_display = (
        'tipo_curso',
        'codigo', 
        'nombre', 
        'intensidad',
    )
    
    list_filter = ['tipo_curso',]
    search_fields = ('nombre',)



class InscripcionCursoInline(admin.TabularInline):
    model = InscripcionCurso
    extra = 1

class EstudianteAdmin(admin.ModelAdmin):
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
    inlines = [InscripcionCursoInline]
    list_display = ('documento', 'nombre', 'apellido')
    search_fields = ['documento', 'nombre', 'apellido']


admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(InscripcionCurso, InscripcionCursoAdmin)