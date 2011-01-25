# -*- coding: utf-8 -*-
from academico.models import Ciclo, NotaCorte, MatriculaCiclo, Calificacion, Corte, Programa, Salon, Competencia, OtrosEstudiosEstudiante, Referencia, MatriculaPrograma, Amonestacion, Estudiante, Profesor, HorarioCurso, Curso
from django.contrib import admin

class CalificacionInline(admin.TabularInline):
    model = Calificacion
    extra = 1
    raw_id_fields = ('curso',)
    fields = ('curso', 'nota_definitiva', 'nota_habilitacion', 'perdio_fallas')



class MatriculaCicloAdmin(admin.ModelAdmin):
    raw_id_fields = ('matricula_programa',)
    fieldsets = [
        (None, {'fields': [
            'fecha_inscripcion', 
            'matricula_programa',
            'ciclo',
            'observaciones']}),
    ]
    list_display = (
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'puesto',
        'ciclo',
        'fecha_inscripcion',
    )
    
    inlines = [CalificacionInline]
    list_filter = ['fecha_inscripcion', 'ciclo']
    search_fields = ('codigo_estudiante', 'ciclo')
    date_hierarchy = 'fecha_inscripcion'


class NotaCorteInline(admin.TabularInline):
    model = NotaCorte
    extra = 1


class CalificacionAdmin(admin.ModelAdmin):
    raw_id_fields = ('curso', 'matricula_ciclo')
    
    fieldsets = [
        (None, {'fields': [
            'curso', 
            'matricula_ciclo',
            'perdio_fallas',
            'nota_definitiva', 
            'nota_habilitacion']}),
    ]
    inlines = [NotaCorteInline]
    list_display = (
        'curso', 
        'codigo_estudiante', 
        'perdio_fallas',
        'nota_definitiva', 
        'nota_habilitacion'
    )
    search_fields = ['curso', 'codigo_estudiante']


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
        'jornada',
        'competencias'
    )
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
    raw_id_fields = ('ciclo', 'profesor')
    fields = ('grupo', 'profesor', 'ciclo')


class CompetenciaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'programa', 
            'sufijo', 
            'nombre', 
            'descripcion', 
            'intensidad', 
            'creditos',
            'periodo']}),
    ]
    inlines = [CursoInline]
    list_display_links = ('codigo', 'nombre',)
    list_display = (
        'codigo', 
        'nombre', 
        'programa', 
        'intensidad', 
        'creditos',
        'periodo',
        'grupos',
    )
    
    list_filter = ['programa', 'intensidad', 'periodo']
    search_fields = ('nombre',)


class OtrosEstudiosEstudianteInline(admin.TabularInline):
    model = OtrosEstudiosEstudiante
    extra = 1


class ReferenciaInline(admin.TabularInline):
    model = Referencia
    extra = 1


class MatriculaProgramaInline(admin.TabularInline):
    model = MatriculaPrograma
    extra = 1
    exclude = ('promedio_acumulado', 'codigo')
  
  
class AmonestacionInline(admin.TabularInline):
    raw_id_fields = ('curso',)
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
            'usuario', 
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
        MatriculaProgramaInline,
        AmonestacionInline
    ]
    list_display = ('documento', 'nombre1', 'apellido1', 'email', 'genero')
    search_fields = ['documento', 'nombre1', 'apellido1']


class MatriculaProgramaAdmin(admin.ModelAdmin):
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
    inlines = [CursoInline]
    list_display = ('documento', 'nombre1', 'apellido1', 'email')
    search_fields = ['documento', 'nombre1', 'apellido1']


class HorarioCursoInline(admin.TabularInline):
    model = HorarioCurso
    extra = 1



class CursoAdmin(admin.ModelAdmin):
    raw_id_fields = ('competencia', 'profesor', 'ciclo')
    fieldsets = [
        (None, {'fields': [
            'competencia', 
            'grupo',
            'profesor',
            'ciclo',
            'estudiantes_esperados']}),
    ]
    
    inlines = [HorarioCursoInline,]
    list_display = (
        'codigo',
        'nombre',
        'profesor',  
        'ciclo',
        'estudiantes_esperados', 
        'estudiantes_inscritos',
        'sesiones',
    )
    list_filter = ['ciclo']
    search_fields = ('competencia',)

class CorteInline(admin.TabularInline):
    model = Corte
    extra = 1
    exclude = ('codigo',)

class CorteAdmin(admin.ModelAdmin):
    raw_id_fields = ('ciclo',)
    
    fieldsets = [
        (None, {'fields': [
            'ciclo',
            'codigo',
            'porcentaje', 
            'fecha_inicio', 
            'fecha_fin',]}),
    ]
    
    list_display = (
        'codigo',
        'porcentaje',         
        'fecha_inicio', 
        'fecha_fin',
        'ciclo'
    )
    search_fields = ('codigo',)
    date_hierarchy = 'fecha_inicio'
    
class CicloAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields': [
            'codigo', 
            'fecha_inicio', 
            'fecha_fin',]}),
    ]
    
    list_display = (
        'codigo', 
        'fecha_inicio', 
        'fecha_fin',
        'cortes'
    )
    
    inlines = [CorteInline]
    search_fields = ('codigo',)
    date_hierarchy = 'fecha_inicio'


#===============================================================================
#AGREGAR VISTAS A INTERFAZ ADMIN 
#===============================================================================
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Corte, CorteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Calificacion, CalificacionAdmin)
admin.site.register(MatriculaCiclo, MatriculaCicloAdmin)
admin.site.register(MatriculaPrograma, MatriculaProgramaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Ciclo, CicloAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)