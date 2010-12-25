# -*- coding: utf-8 -*-
from academico.models import *
from django.contrib import admin


class NotaCorteInline(admin.TabularInline):
  model = NotaCorte
  extra = 1


class MatriculaProgramaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'fecha_expedicion', 
              'inscripcion_estudiante',
              'programa',
              'fecha_vencimiento',
              'promedio_periodo',
              'puesto',
              'observaciones']}),
  ]
  list_display = ('fecha_expedicion', 'inscripcion_estudiante', 'programa', 'promedio_periodo')
  list_filter = ['fecha_expedicion', 'programa']
  search_fields = ('inscripcion_estudiante',)
  date_hierarchy = 'fecha_expedicion'



class MatriculaCursoAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'curso', 
              'inscripcion_estudiante',
              'perdio_fallas',
              'nota_definitiva', 
              'nota_habilitacion']}),
  ]
  inlines = [NotaCorteInline]
  list_display = ('curso', 'inscripcion_estudiante', 'perdio_fallas',
              'nota_definitiva', 'nota_habilitacion')
  search_fields = ['curso', 'inscripcion_estudiante']

class CorteAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'codigo', 
              'porcentaje',
              'fecha_inicio',
              'fecha_fin']}),
  ]
  list_display = ('codigo', 'porcentaje', 'fecha_inicio', 'fecha_fin')


class ProgramaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'tipo_programa', 
              'codigo', 
              'nombre', 
              'descripcion', 
              'titulo', 
              'resolucion',
              'snies']}),
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
  list_display = ('tipo_programa', 'codigo', 'nombre', 'periodicidad', 'duracion', 'jornada')
  search_fields = ['codigo', 'nombre']
  list_filter = ['tipo_programa', 'jornada', 'periodicidad']
  


class SalonAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'codigo', 
              'descripcion', 
              'capacidad', 
              'tipo_salon']}),
  ]
  list_display = ('codigo', 'descripcion', 'capacidad', 'tipo_salon')
  search_fields = ['codigo', 'descripcion']
  list_filter = ['tipo_salon']


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
  list_display = ('codigo', 'nombre', 'programa', 'intensidad', 'modulo', 'periodo')
  list_filter = ['programa', 'modulo']
  search_fields = ('nombre',)


class OtrosEstudiosEstudianteInline(admin.TabularInline):
  model = OtrosEstudiosEstudiante
  extra = 1


class ReferenciaInline(admin.TabularInline):
  model = Referencia
  extra = 1


class InscripcionEstudianteInline(admin.TabularInline):
  model = InscripcionEstudiante
  extra = 1
  
  
class AmonestacionInline(admin.TabularInline):
  model = Amonestacion
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
              'usuario', 
              'contrasena'], 
              'classes': ['collapse']}),
  ]
  inlines = [ OtrosEstudiosEstudianteInline, 
              ReferenciaInline,
              InscripcionEstudianteInline,
              AmonestacionInline]
  list_display = ('documento', 'nombre', 'apellido')
  search_fields = ['documento', 'nombre', 'apellido']
  

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
              'usuario', 
              'contrasena'],
              'classes': ['collapse']}),
  ]
  inlines = [ExperienciaLaboralProfesorInline, OtrosEstudiosProfesorlInline]
  list_display = ('documento', 'nombre', 'apellido')
  search_fields = ['documento', 'nombre', 'apellido']


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
              'codigo',
              'profesor',
              'fecha_inicio', 
              'fecha_fin',              
              'estudiantes_esperados',
              'estudiantes_inscritos']}),
  ]
  inlines = [HorarioCursoInline, SesionCursoInline]
  list_display = ('codigo', 'profesor', 'estudiantes_esperados', 
  					'estudiantes_inscritos', 'fecha_inicio', 'fecha_fin')
  search_fields = ('competencia',)

class AsistenciaAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': [
              'sesion_curso', 
              'inscripcion_estudiante', 
              'asistio', 
              'observaciones']}),
  ]
  list_display = ('sesion_curso', 'inscripcion_estudiante', 'asistio', 
  					'observaciones')
  search_fields = ('sesion_curso', 'inscripcion_estudiante')


admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Corte, CorteAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(MatriculaCurso, MatriculaCursoAdmin)
admin.site.register(MatriculaPrograma, MatriculaProgramaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)