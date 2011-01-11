# -*- coding: utf-8 -*-
from academico.models import Semestre, NotaCorte, MatriculaPrograma, MatriculaCurso, Corte, Programa, Salon, Competencia, OtrosEstudiosEstudiante, Referencia, InscripcionEstudiante, Amonestacion, Estudiante, ExperienciaLaboralProfesor, OtrosEstudiosProfesor, Profesor, HorarioCurso, Curso, SesionCurso, Asistencia
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
    list_display = (
        'fecha_expedicion', 
        'inscripcion_estudiante', 
        'programa', 
        'promedio_periodo'
    )
    
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
    list_display = (
        'curso', 
        'inscripcion_estudiante', 
        'perdio_fallas',
        'nota_definitiva', 
        'nota_habilitacion'
    )
    search_fields = ['curso', 'inscripcion_estudiante']


class ProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [     
            'codigo',             
            'nombre',
            'tipo_programa', 
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
    list_display = (
        'codigo',
        'nombre',
        'tipo_programa',  
        'periodicidad', 
        'duracion', 
        'jornada')
    list_display_links = ('codigo', 'nombre')
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

class CursoInline(admin.TabularInline):
    model = Curso
    extra = 1
    raw_id_fields = ('competencia',)
    fields = ('grupo', 'profesor', 'semestre')
    
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
    inlines = [CursoInline]
    list_display_links = ('codigo', 'nombre',)
    list_display = (
        'codigo', 
        'nombre', 
        'programa', 
        'intensidad', 
        'modulo', 
        'periodo',
    )
    
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
    exclude = ('promedio_acumulado')
  
  
class AmonestacionInline(admin.TabularInline):
    model = Amonestacion
    extra = 1


class EstudianteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identificacion', { 'fields': [ 
            'nombre1',
            'nombre2', 
            'apellido1', 
            'apellido2', 
            'genero', 
            'tipo_documento', 
            'documento', 
            'lugar_expedicion',
            'fecha_nacimiento', 
            'lugar_nacimiento']}),
        ('Requisitos', {'fields': [
            'fotocopia_documento', 
            'fotocopia_diploma', 
            'foto'], 
            'classes': ['collapse']}),
        ('Informacion de ubicacion', {'fields': [
            'direccion', 
            'lugar_residencia',
            'estrato',
            'telefono', 
            'movil',
            'email', 
            'web'], 
            'classes': ['collapse']}),
        ('Informacion de acceso', {'fields': [
            'contrasena'], 
            'classes': ['collapse']}),
        ('Informacion adicional', {'fields': [
            'sisben',
            'discapacidad', 
            'etnia'], 
            'classes': ['collapse']}),
    ]
    inlines = [
        OtrosEstudiosEstudianteInline, 
        ReferenciaInline,
        InscripcionEstudianteInline,
        AmonestacionInline
    ]
    list_display = ('documento', 'nombre1', 'apellido1', 'email', 'genero', 'usuario')
    search_fields = ['documento', 'nombre1', 'apellido1']


class EstudianteInscripcionAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields':[
                                   'codigo',
                                   'fecha_inscripcion',
                                   'estado'
                                   ]}),
                 ]
    
    list_display = (
                    'codigo',
                    'nombre_estudiante',
                    'fecha_inscripcion',
                    'estado'
                    )
    
    search_fields = ('codigo', 'estado')

class ExperienciaLaboralProfesorInline(admin.TabularInline):
    model = ExperienciaLaboralProfesor
    extra = 1


class OtrosEstudiosProfesorlInline(admin.TabularInline):
    model = OtrosEstudiosProfesor
    extra = 1


class ProfesorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identificacion', {'fields': [
            'nombre1',
            'nombre2', 
            'apellido1', 
            'apellido2', 
            'genero', 
            'tipo_documento', 
            'documento', 
            'lugar_expedicion',
            'fecha_nacimiento', 
            'lugar_nacimiento', 
            'foto']}),
        ('Informacion de contacto', {'fields': [
            'direccion', 
            'lugar_residencia', 
            'telefono', 
            'movil',
            'email', 
            'web'],
            'classes': ['collapse']}),
        ('Informacion de acceso', {'fields': [
            'contrasena'],
            'classes': ['collapse']}),
    ]
    inlines = [ExperienciaLaboralProfesorInline, OtrosEstudiosProfesorlInline]
    list_display = ('documento', 'nombre1', 'apellido1', 'email', 'usuario')
    search_fields = ['documento', 'nombre1', 'apellido1']


class HorarioCursoInline(admin.TabularInline):
    model = HorarioCurso
    extra = 1


class SesionCursoInline(admin.TabularInline):
    model = SesionCurso
    extra = 1


class CursoAdmin(admin.ModelAdmin):
    raw_id_fields = ('competencia', 'profesor', 'semestre')
    fieldsets = [
        (None, {'fields': [
            'competencia', 
            'grupo',
            'profesor',
            'semestre',         
            'estudiantes_esperados',
            'estudiantes_inscritos']}),
    ]
    
    inlines = [HorarioCursoInline, SesionCursoInline]
    list_display_links = ('codigo', 'competencia')
    list_display = (
        'codigo',
        'competencia',
        'profesor', 
        'estudiantes_esperados', 
        'estudiantes_inscritos', 
        'semestre', 
    )
    
    search_fields = ('competencia',)

class AsistenciaAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields': [
            'sesion_curso', 
            'inscripcion_estudiante', 
            'asistio', 
            'observaciones']}),
    ]
    
    list_display = (
        'sesion_curso', 
        'inscripcion_estudiante', 
        'asistio', 
        'observaciones'
    )
    
    search_fields = ('sesion_curso', 'inscripcion_estudiante')

class CorteInline(admin.TabularInline):
    model = Corte
    extra = 1
    exclude = ('codigo',)

class SemestreAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields': [
            'codigo', 
            'fecha_inicio', 
            'fecha_fin',]}),
    ]
    
    list_display = (
        'codigo',
        'cortes', 
        'fecha_inicio', 
        'fecha_fin',
    )
    
    inlines = [CorteInline]
    search_fields = ('codigo',)
    date_hierarchy = 'fecha_inicio'



admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(MatriculaCurso, MatriculaCursoAdmin)
admin.site.register(MatriculaPrograma, MatriculaProgramaAdmin)
admin.site.register(InscripcionEstudiante, EstudianteInscripcionAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Semestre, SemestreAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)