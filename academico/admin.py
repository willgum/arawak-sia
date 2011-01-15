# -*- coding: utf-8 -*-
from academico.models import Ciclo, NotaCorte, InscripcionProgramaCiclo, Calificacion, Corte, Programa, Salon, Competencia, OtrosEstudiosEstudiante, Referencia, InscripcionEstudiantePrograma, Amonestacion, Estudiante, ExperienciaLaboralProfesor, OtrosEstudiosProfesor, Profesor, HorarioCurso, Curso, SesionCurso, Asistencia
from django.contrib import admin

class CalificacionInline(admin.TabularInline):
    model = Calificacion
    extra = 1
    raw_id_fields = ('curso',)
    fields = ('curso', 'nota_definitiva', 'nota_habilitacion', 'perdio_fallas')



class InscripcionProgramaCicloAdmin(admin.ModelAdmin):
    raw_id_fields = ('inscripcion_estudiante_programa',)
    fieldsets = [
        (None, {'fields': [
            'fecha_inscripcion', 
            'inscripcion_estudiante_programa',
            'ciclo',
            'puesto',
            'observaciones']}),
    ]
    list_display = (
        'fecha_inscripcion', 
        'nombre_estudiante',
        'nombre_programa',
        'ciclo'
    )
    
    inlines = [CalificacionInline]
    list_filter = ['fecha_inscripcion', 'ciclo']
    search_fields = ('inscripcion_estudiante_programa', 'ciclo')
    date_hierarchy = 'fecha_inscripcion'


class NotaCorteInline(admin.TabularInline):
    model = NotaCorte
    extra = 1


class CalificacionAdmin(admin.ModelAdmin):
    raw_id_fields = ('curso', 'inscripcion_programa_ciclo')
    
    fieldsets = [
        (None, {'fields': [
            'curso', 
            'inscripcion_programa_ciclo',
            'perdio_fallas',
            'nota_definitiva', 
            'nota_habilitacion']}),
    ]
    inlines = [NotaCorteInline]
    list_display = (
        'curso', 
        'inscripcion_programa_ciclo', 
        'perdio_fallas',
        'nota_definitiva', 
        'nota_habilitacion'
    )
    search_fields = ['curso', 'inscripcion_programa_ciclo']


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
    fields = ('grupo', 'profesor', 'ciclo')


class CompetenciaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'programa', 
            'codigo', 
            'nombre', 
            'descripcion', 
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
        'periodo',
    )
    
    list_filter = ['programa', 'intensidad', 'periodo']
    search_fields = ('nombre',)


class OtrosEstudiosEstudianteInline(admin.TabularInline):
    model = OtrosEstudiosEstudiante
    extra = 1


class ReferenciaInline(admin.TabularInline):
    model = Referencia
    extra = 1


class InscripcionEstudianteProgramaInline(admin.TabularInline):
    model = InscripcionEstudiantePrograma
    extra = 1
    exclude = ('promedio_acumulado', 'codigo')
  
  
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
        ('Informacion adicional', {'fields': [
            'sisben',
            'discapacidad', 
            'etnia'], 
            'classes': ['collapse']}),
    ]
    inlines = [
        OtrosEstudiosEstudianteInline, 
        ReferenciaInline,
        InscripcionEstudianteProgramaInline,
        AmonestacionInline
    ]
    list_display = ('documento', 'nombre1', 'apellido1', 'email', 'genero')
    search_fields = ['documento', 'nombre1', 'apellido1']


class InscripcionEstudianteProgramaAdmin(admin.ModelAdmin):
    raw_id_fields = ('estudiante', 'programa')
    
    fieldsets = [
                 (None, {'fields':[
                                   'estudiante',
                                   'programa',
                                   'fecha_inscripcion',
                                   'fecha_vencimiento',
                                   'estado',
                                   'becado',
                                   ]}),
                 ]
    
    list_display = (
                    'codigo',
                    'nombre_estudiante',
                    'nombre_programa',
                    'fecha_inscripcion',
                    'estado'
                    )
    
    search_fields = ('codigo', 'nombre_programa', 'estado')

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
    ]
    inlines = [ExperienciaLaboralProfesorInline, OtrosEstudiosProfesorlInline]
    list_display = ('documento', 'nombre1', 'apellido1', 'email')
    search_fields = ['documento', 'nombre1', 'apellido1']


class HorarioCursoInline(admin.TabularInline):
    model = HorarioCurso
    extra = 1


class SesionCursoInline(admin.TabularInline):
    model = SesionCurso
    extra = 1


class CursoAdmin(admin.ModelAdmin):
    raw_id_fields = ('competencia', 'profesor', 'ciclo')
    fieldsets = [
        (None, {'fields': [
            'competencia', 
            'grupo',
            'profesor',
            'ciclo',
            'estudiantes_inscritos']}),
    ]
    
    inlines = [HorarioCursoInline, SesionCursoInline]
    list_display_links = ('codigo', 'competencia_nombre')
    list_display = (
        'codigo',
        'competencia_nombre',
        'profesor',  
        'ciclo', 
        'estudiantes_inscritos',
    )
    
    search_fields = ('competencia',)

class AsistenciaAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields': [
            'sesion_curso', 
            'inscripcion_estudiante_programa', 
            'asistio', 
            'observaciones']}),
    ]
    
    list_display = (
        'sesion_curso', 
        'inscripcion_estudiante_programa', 
        'asistio', 
        'observaciones'
    )
    
    search_fields = ('sesion_curso', 'inscripcion_estudiante_programa')

class CorteInline(admin.TabularInline):
    model = Corte
    extra = 1
    exclude = ('codigo',)

class CicloAdmin(admin.ModelAdmin):
    
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


#===============================================================================
#AGREGAR VISTAS A INTERFAZ ADMIN 
#===============================================================================
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Calificacion, CalificacionAdmin)
admin.site.register(InscripcionProgramaCiclo, InscripcionProgramaCicloAdmin)
admin.site.register(InscripcionEstudiantePrograma, InscripcionEstudianteProgramaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Ciclo, CicloAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)