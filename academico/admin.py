# -*- coding: utf-8 -*-
from academico.models import *
from django.contrib import admin


class CorteInline(admin.TabularInline):
  model = Corte
  extra = 1


class MatriculaCursoAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'curso', 
              'matricula_estudiante',
              'perdio_fallas',
              'nota_definitiva', 
              'nota_habilitacion']}),
  ]
  inlines = [CorteInline]


class ProgramaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'tipo_programa', 
              'codigo', 
              'nombre', 
              'descripcion', 
              'titulo', 
              'resolucion']}),
    ('Horario', {'fields': [
              'periodicidad', 
              'duracion', 
              'jornada'], 
              'classes': ['collapse']}),
    ('Informacion adicional', {'fields': [
              'actitudes', 
              'perfil_profesional', 
              'funciones'], 
              'classes': ['collapse']}),
  ]
  list_display = ('codigo', 'nombre', 'jornada')


class SalonAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'codigo', 
              'descripcion', 
              'capacidad', 
              'tipo_salon']}),
  ]


class CompetenciaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'programa', 
              'codigo', 
              'nombre', 
              'descripcion', 
              'modulo', 
              'intensidad', 
              'periodo']}),
  ]
    

class OtrosEstudiosEstudianteInline(admin.TabularInline):
  model = OtrosEstudiosEstudiante
  extra = 1


class ReferenciaInline(admin.TabularInline):
  model = Referencia
  extra = 1


class EstudianteAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,  {'fields': ['programa']}),
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
    ('Requisitos', {'fields': [
              'fotocopia_documento', 
              'fotocopia_diploma', 
              'foto'], 
              'classes': ['collapse']}),
    ('Informacion de contacto', {'fields': [
              'direccion', 
              'lugar_residencia', 
              'telefono', 
              'email', 
              'web'], 
              'classes': ['collapse']}),
    ('Informacion de acceso', {'fields': [
              'codigo', 
              'usuario', 
              'contrasena'], 
              'classes': ['collapse']}),
  ]
  inlines = [OtrosEstudiosEstudianteInline, ReferenciaInline]


class PagoInline(admin.TabularInline):
  model = Pago
  extra = 1
  
  
class AmonestacionInline(admin.TabularInline):
  model = Amonestacion
  extra = 1
  

class MatriculaEstudianteAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,  {'fields': [  
              'fecha_matricula', 
              'estudiante', 
              'estado',
              'becado',
              'valor_inscripcion',
              'valor_matricula',
              'cuotas',
              'letras']}),
  ]
  inlines = [PagoInline, AmonestacionInline] 


class ExperienciaLaboralProfesorInline(admin.TabularInline):
  model = ExperienciaLaboralProfesor
  extra = 1


class OtrosEstudiosProfesorlInline(admin.TabularInline):
  model = OtrosEstudiosProfesor
  extra = 1


class ProfesorAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Informacion Personal', {'fields': [
              'nombre', 
              'apellido', 
              'sexo', 
              'tipo_documento', 
              'documento', 
              'lugar_expedicion',
              'fecha_nacimiento', 
              'lugar_nacimiento', 
              'foto'], 
              'classes': ['collapse']}),
    ('Informacion de contacto', {'fields': [
              'direccion', 
              'lugar_residencia', 
              'telefono', 
              'email', 
              'web'],
              'classes': ['collapse']}),
    ('Informacion de acceso', {'fields': [
              'codigo', 
              'usuario', 
              'contrasena'],
              'classes': ['collapse']}),
  ]
  inlines = [ExperienciaLaboralProfesorInline, OtrosEstudiosProfesorlInline] 


class HorarioCursoInline(admin.TabularInline):
  model = HorarioCurso
  extra = 1


class SesionCursoInline(admin.TabularInline):
  model = SesionCurso
  extra = 1


class CursoAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'competencia', 
              'grupo', 
              'fecha_inicio', 
              'fecha_fin', 
              'profesor',
              'estudiantes']}),
  ]
  inlines = [HorarioCursoInline, SesionCursoInline]

class AsistenciaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'sesion_curso', 
              'matricula_estudiante', 
              'asistio', 
              'observaciones']}),
  ]

admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(MatriculaEstudiante, MatriculaEstudianteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(MatriculaCurso, MatriculaCursoAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
