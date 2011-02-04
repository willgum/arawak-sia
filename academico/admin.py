# -*- coding: utf-8 -*-
from academico.models import Ciclo, NotaCorte, MatriculaCiclo, Calificacion, Corte, Programa, Salon, Competencia, EstudioComplementario, Referencia, MatriculaPrograma, Amonestacion, Estudiante, Profesor, HorarioCurso, Curso
from django.contrib import admin

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

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
            'nota_definitiva', 
            'nota_habilitacion',
            'perdio_fallas',
            ]}),
    ]
    inlines = [NotaCorteInline]
    list_display = (
        'curso', 
        'codigo_estudiante', 
        'nota_definitiva', 
        'nota_habilitacion',
        'fallas',
        'perdio_fallas',
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


class EstudioComplementarioInline(admin.TabularInline):
    model = EstudioComplementario
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
        ('Informacion adicional', {'fields': [
            'sisben',
            'discapacidad', 
            'etnia'], 
            'classes': ['collapse']}),
    ]
    inlines = [
        EstudioComplementarioInline, 
        ReferenciaInline,
        MatriculaProgramaInline,
        AmonestacionInline
    ]
    list_display = ('documento', 'nombre1', 'apellido1', 'usuario', 'email', 'genero')
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
    list_display = ('documento', 'nombre1', 'apellido1', 'usuario', 'email')
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
            'esperados']}),
    ]
    
    inlines = [HorarioCursoInline,]
    list_display = (
        'codigo',
        'nombre',
        'profesor',  
        'ciclo',
        'esperados', 
        'inscritos',
        'sesiones',
    )
    list_filter = ['ciclo']
    search_fields = ('competencia',)

class CorteInline(admin.TabularInline):
    model = Corte
    extra = 1

class CorteAdmin(admin.ModelAdmin):
    raw_id_fields = ('ciclo',)
    
    fieldsets = [
        (None, {'fields': [
            'ciclo',
            'sufijo',
            'porcentaje', 
            'fecha_inicio', 
            'fecha_fin',]}),
    ]
    
    list_display = (
        'codigo_corte',
        'porcentaje',         
        'fecha_inicio', 
        'fecha_fin',
        'ciclo',
        'corteActual'        
    )
    search_fields = ('codigo_corte',)
    date_hierarchy = 'fecha_inicio'
    

class ButtonableModelAdmin(admin.ModelAdmin):
    """
   A subclass of this admin will let you add buttons (like history) in the
   change view of an entry.
   http://www.theotherblog.com/Articles/2009/06/02/extending-the-django-admin-interface/
    """
    buttons=[]

    def change_view(self, request, object_id, extra_context={}):
        extra_context['buttons']=self.buttons
        return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context)

    def __call__(self, request, url):
        if url is not None:
            import re
            res=re.match('(.*/)?(?P<id>\d+)/(?P<command>.*)', url)
            if res:
                if res.group('command') in [b.func_name for b in self.buttons]:
                    obj = self.model._default_manager.get(pk=res.group('id'))
                    getattr(self, res.group('command'))(obj)
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])

        return super(ButtonableModelAdmin, self).__call__(request, url)

class CicloAdmin(ButtonableModelAdmin):
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

    def promocion(self, obj):
#        url = "/admin" + "/".join(str( obj._meta ).split(".")) + "/" + str(obj.id) + "/"
        url = "/admin/academico/ciclo/promocion"
        return HttpResponseRedirect( url )
    promocion.url = "/admin/academico/ciclo/promocion"    #puts this on the end of the admin URL.
    promocion.short_description='Promoción ciclo'
    buttons = [ promocion,]

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