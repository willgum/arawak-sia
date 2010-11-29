# -*- coding: utf-8 -*-
from academico.models import *
from django.contrib import admin

class MatriculaCursoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['curso', 'estudiante', 'nota']}),
    ]


class ProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['tipo_programa', 'codigo', 'nombre', 'descripcion', 'titulo', 'resolucion']}),
        ('Horario', {'fields': ['periodicidad', 'duracion', 'jornada'], 'classes': ['collapse']}),
        ('Extra', {'fields': ['actitudes', 'perfil_profesional', 'funciones'], 'classes': ['collapse']}),
    ]
    list_display = ('codigo', 'nombre', 'jornada')


class SalonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['codigo', 'descripcion', 'capacidad', 'tipo_salon']}),
    ]


class CompetenciaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['programa', 'codigo', 'nombre', 'descripcion', 'modulo', 'periodo']}),
    ]
    

class OtrosEstudiosInline(admin.TabularInline):
  model = OtrosEstudios
  extra = 1


class ReferenciaInline(admin.TabularInline):
  model = Referencia
  extra = 1


class EstudianteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion Personal', 
        {'fields': ['nombre', 'apellido', 'sexo', 'tipo_documento', 'documento', 'lugar_expedicion',        
        'fecha_nacimiento', 'lugar_nacimiento', 'foto'], 
        'classes': ['collapse']}),
        ('Informacion de contacto', 
        {'fields': ['direccion', 'lugar_residencia', 'telefono', 'email', 'web'], 
        'classes': ['collapse']}),
    ]
    inlines = [OtrosEstudiosInline, ReferenciaInline]


class PagoInline(admin.TabularInline):
  model = Pago
  extra = 1
  
  
class AmonestacionInline(admin.TabularInline):
  model = Amonestacion
  extra = 1
  
class MatriculaEstudianteAdmin(admin.ModelAdmin):
    fieldsets = [
      (None,  {'fields': ['fecha_inscripcion', 'estudiante', 'estado', 'programa', 'codigo', 'usuario', 'contrasena']}),
    ]
    inlines = [PagoInline, AmonestacionInline] 


class ProfesorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion Personal', 
        {'fields': ['nombre', 'apellido', 'sexo', 'tipo_documento', 'documento', 'lugar_expedicion',        
        'fecha_nacimiento', 'lugar_nacimiento', 'foto'], 
        'classes': ['collapse']}),
        ('Informacion de contacto', 
        {'fields': ['direccion', 'lugar_residencia', 'telefono', 'email', 'web'], 
        'classes': ['collapse']}),
    ]

class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1

    
class CursoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['competencia', 'grupo', 'numero_estudiantes', 'fecha_inicio', 'fecha_fin', 
        'profesor']}),
    ]
    inlines = [SesionInline]


admin.site.register(MatriculaEstudiante, MatriculaEstudianteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(MatriculaCurso, MatriculaCursoAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Estudiante, EstudianteAdmin)