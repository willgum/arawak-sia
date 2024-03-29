# -*- coding: utf-8 -*-
from academico.models import Ciclo, NotaCorte, MatriculaCiclo, Calificacion, Corte, Programa, Salon, Materia, EstudioComplementario, Referencia, MatriculaPrograma, Amonestacion, Estudiante, Profesor, HorarioCurso, Curso, Institucion, Funcionario, TipoPrograma, TipoNotaConceptual, ProfesorExperiencia, TipoValoracion
from academico.models import Sede
from django.contrib import admin
from django.http import HttpResponseRedirect

class ButtonableModelAdmin(admin.ModelAdmin):
    """
   A subclass of this admin will let you add buttons (like history) in the
   change view of an entry.
   http://www.theotherblog.com/Articles/2009/06/02/extending-the-django-admin-interface/
    """
    buttons=[]
    buttons_list=[]
    
    def changelist_view(self, request, extra_context={}):
        extra_context['buttons']=self.buttons_list
        return super(ButtonableModelAdmin, self).changelist_view(request, extra_context)
    
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


class CalificacionInline(admin.TabularInline):
    model = Calificacion
    extra = 1
    raw_id_fields = ('curso',)
    fields = ('curso', 'nota_definitiva', 'nota_habilitacion', 'perdio_fallas', 'tipo_aprobacion')
    readonly_fields = ('nota_definitiva', 'nota_habilitacion')


class MatriculaCicloAdmin(ButtonableModelAdmin):
    raw_id_fields = ('matricula_programa', 'ciclo')
    readonly_fields = ('sede',
                       'nombre_estudiante', 
                       'promedio_ciclo', 
                       'cursos_inscritos', 
                       'nombre_programa',)
    fieldsets = [
        ('Resumen', {'fields': [
            'nombre_estudiante',
            'nombre_programa',
            'promedio_ciclo',
            'cursos_inscritos',
            'sede',]}),
        ('Información básica', {'fields': [
            'fecha_inscripcion', 
            'matricula_programa',
            'ciclo',
            'observaciones']}),
    ]
    list_display_links = ('nombre_estudiante',)
    
    list_display = (
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'promedio_ciclo',
        'cursos_inscritos',
        'puesto',
        'ciclo',
        'total_creditos',
        'fecha_inscripcion',
    )
    
    
    inlines = [CalificacionInline]
    list_filter = ['ciclo', 'fecha_inscripcion',]
    search_fields = ('matricula_programa__programa__id', 
                     'matricula_programa__codigo', 
                     'matricula_programa__programa__nombre',
                     'matricula_programa__estudiante__nombre1', 
                     'matricula_programa__estudiante__nombre2', 
                     'matricula_programa__estudiante__apellido1', 
                     'matricula_programa__estudiante__apellido2',)
    date_hierarchy = 'fecha_inscripcion'
    
    def constancia(self, obj):
        url = "/admin/academico/matriculaciclo/constancia"
        return HttpResponseRedirect( url )
    constancia.url = "/admin/academico/matriculaciclo/constancia"    #puts this on the end of the admin URL.
    constancia.short_description='Imprimir constancia'
    
    buttons = [constancia, ]
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)


class NotaCorteInline(admin.TabularInline):
    raw_id_fields = ('corte',)
    model = NotaCorte
    extra = 1


class CalificacionAdmin(admin.ModelAdmin):
    raw_id_fields = ('curso', 'matricula_ciclo')
    
    fieldsets = [
        ('Información básica', {'fields': [
            'nombre_estudiante',
            'codigo_ciclo',
            'nota_definitiva',
            'curso', 
            'matricula_ciclo', 
            'nota_habilitacion',
            'perdio_fallas',
            'tipo_aprobacion',
            ]}),
    ]
    inlines = [NotaCorteInline]
    list_display = (
        'codigo_curso',
        'nombre_materia', 
        'nombre_estudiante', 
        'codigo_ciclo',
        'nota_definitiva', 
        'nota_habilitacion',
        'fallas',
        'perdio_fallas',
    )
    
    readonly_fields = ('nombre_estudiante', 'nota_definitiva', 'codigo_ciclo')
    search_fields = ['curso__materia__codigo', 'matricula_ciclo__ciclo__codigo', 'curso__materia__nombre', 
                     'matricula_ciclo__matricula_programa__estudiante__nombre1', 'matricula_ciclo__matricula_programa__estudiante__nombre2', 
                     'matricula_ciclo__matricula_programa__estudiante__apellido1', 'matricula_ciclo__matricula_programa__estudiante__apellido2',]
    list_filter = ['perdio_fallas']


class TipoProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [     
            'codigo',             
            'nombre']}),
    ]
    list_display = (
            'codigo',             
            'nombre',
    )
    list_display_links = ('codigo', 'nombre')
    search_fields = ['codigo', 'nombre']
    

class ProgramaAdmin(admin.ModelAdmin):
    raw_id_fields = ('sede',)
    
    fieldsets = [
        ('Información básica', {'fields': [     
            'sede',
            'nombre',
            'codigo',             
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
            'horas_bienestar',
            'aptitudes', 
            'perfil_profesional', 
            'funciones'], 
            'classes': ['collapse']}),
    ]
    list_display = (
        'codigo',
        'nombre',
        'tipo_programa',
        'sede',
        'periodicidad', 
        'duracion', 
        'materias',
    )
    list_display_links = ('nombre',)
    search_fields = ['codigo', 'nombre']
    list_filter = ['tipo_programa', 'periodicidad', 'sede']
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

class SalonAdmin(admin.ModelAdmin):
    raw_id_fields = ('sede',)
    fieldsets = [
        ('Información básica', {'fields': [
            'codigo',
            'sede', 
            'descripcion', 
            'capacidad', 
            'tipo_salon',
            'mapa']}),
    ]
    list_display = ('codigo', 'sede', 'descripcion', 'capacidad', 'tipo_salon')
    search_fields = ['codigo',]
    list_filter = ['tipo_salon',]
        
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

    
    
class MateriaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información básica', {'fields': [
            'nombre',
            'codigo',
            'programa',
            'descripcion', 
            'intensidad_semanal',
            'intensidad_ciclo', 
            'creditos',
            'tipo_valoracion']}),
        ('Requisitos', {'fields': ('requisito',)})
    )
    
    filter_horizontal = ('programa', 'requisito',)
    
    list_display_links = ('nombre',)
    list_display = (
        'codigo', 
        'nombre',  
        'intensidad_ciclo', 
        'creditos'
    )
    
    search_fields = ('nombre', 'codigo')
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)


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
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)



class EstudianteAdmin(ButtonableModelAdmin):
    fieldsets = [
        ('Identificacion', { 'fields': [ 
            'nombre1',
            'nombre2', 
            'apellido1', 
            'apellido2', 
            'tipo_documento', 
            'documento', 
            'lugar_expedicion',
            'genero', 
            'grupo_sanguineo', 
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
    

class MatriculaProgramaAdmin(ButtonableModelAdmin):
    raw_id_fields = ('estudiante', 'programa')
    
    fieldsets = [
                 ('Información básica', {'fields':[
                                   'estudiante',
                                   'programa',
                                   'fecha_inscripcion',
                                   'fecha_vencimiento',
                                   'usuario', 
                                   'estado',
                                   'promedio_acumulado',
                                   'horas_bienestar',
                                   'becado',
                                   ]}),
                 ]
    
    list_display = (
                    'codigo',
                    'usuario',
                    'nombre_estudiante',
                    'nombre_programa',
                    'promedio_acumulado',
                    'fecha_inscripcion',
                    'estado'
                    )
    
    date_hierarchy = 'fecha_inscripcion'
    
    readonly_fields = ('horas_bienestar', 'promedio_acumulado', 'usuario',)
    
    list_filter = ['estado', 'programa']
    search_fields = ('codigo', 'programa__nombre', 'estado__nombre', 'estudiante__nombre1', 'estudiante__apellido1')
    
    def inscritos(self, request, obj):
        obj.inscritos()
    inscritos.url = "/admin/academico/matriculaprograma/inscritos"
    inscritos.short_description='Estudiantes inscritos'
    
    buttons_list = [inscritos, ]
    
    def imprimircarnet(self, request, obj):
        obj.imprimirCarnet()
        
    imprimircarnet.short_description='Imprimir Carnet'
    
    buttons = [imprimircarnet, ]


class ExperienciaProfesorInline(admin.TabularInline):
    model = ProfesorExperiencia
    extra = 1
    fields = ('cargo', 'empresa', 'fecha_inicio', 'fecha_fin', 'actualmente')
    

class ProfesorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identificacion', {'fields': [
            'nombre1',
            'nombre2', 
            'apellido1', 
            'apellido2', 
            'tipo_documento', 
            'documento', 
            'lugar_expedicion',
            'genero', 
            'grupo_sanguineo', 
            'fecha_nacimiento', 
            'lugar_nacimiento', 
            'foto',
            'titulo',
            'perfil_profesional',]}),
        ('Informacion de contacto', {'fields': [
            'direccion', 
            'lugar_residencia', 
            'telefono', 
            'movil',
            'email', 
            'web'],
            'classes': ['collapse']}),
    ]
    inlines = [ExperienciaProfesorInline, ]
    list_display = ('documento', 'nombre1', 'apellido1', 'usuario', 'email')
    search_fields = ['documento', 'nombre1', 'apellido1']
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)


class HorarioCursoInline(admin.TabularInline):
    model = HorarioCurso
    extra = 1
    
class estudiantesInscritosInline(admin.TabularInline):
    model = Calificacion
    verbose_name_plural = 'Estudiantes inscritos'
    fields = ['matricula_ciclo',
              'nombre_estudiante',
              'tipo_aprobacion',
              'nota_definitiva',
              'nota_habilitacion',
              'fallas',
              'perdio_fallas']
    raw_id_fields = ('matricula_ciclo',)
    readonly_fields = ['nombre_estudiante', 'nota_definitiva', 'tipo_aprobacion']
    extra = 0    

class CursoAdmin(admin.ModelAdmin):
    raw_id_fields = ('materia', 'profesor', 'ciclo')
    fieldsets = [
        ('Información básica', {'fields': [
            'materia', 
            'grupo',
            'profesor',
            'ciclo',
            'esperados']})
    ]    
    inlines = [HorarioCursoInline, estudiantesInscritosInline, ]
    
    list_display_links = ('nombre_curso',)
    list_display = (
        'codigo',
        'grupo',
        'nombre_curso',
        'profesor',  
        'ciclo',
        'inscritos',
        'promedio',
    )
    
    
    
    list_filter = ['ciclo', 'grupo']
    search_fields = ('materia__codigo', 
                     'materia__nombre', 
                     'profesor__nombre1', 
                     'profesor__nombre2', 
                     'profesor__apellido1', 
                     'profesor__apellido2',)

class CorteInline(admin.TabularInline):
    model = Corte
    extra = 1

class CorteAdmin(admin.ModelAdmin):
    raw_id_fields = ('ciclo',)
    
    fieldsets = [
        ('Información básica', {'fields': [
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
    )
    list_filter =  ['ciclo',]
    search_fields = ('codigo_corte',)
    

class FuncionarioInline(admin.TabularInline):
    model = Funcionario
    extra = 1
    fields = ('nombre', 'tipo_documento', 'documento', 'lugar_expedicion', 'tipo_funcionario')


class TipoNotaConceptualAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
            'codigo',
            'nombre',]}),
    ]
    
    list_display = (
        'codigo',
        'nombre',      
    )
    
    search_fields = ('codigo', 'nombre')


class TipoValoracionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
            'nombre',
            'nota_minima',
            'nota_maxima',
            'nota_aprobacion',
            ]}),
    ]
    
    list_display = (
        'nombre',
        'nota_minima',
        'nota_maxima',
        'nota_aprobacion',      
    )
    
    search_fields = ('nombre',)


class SedeAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Información básica', {'fields': [
            'nombre',
            'direccion',
            'ciudad',
            'departamento',
            'telefono',
            'email',
            'web'
            ]}),
    ]
    
    list_display = (
        'nombre',
        'direccion',
        'ciudad',
        'departamento',
        'telefono', 
        'email',
        'web'
    )

    search_fields = ('nombre',)
    
class InstitucionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
            'nombre',
            'nit',
            'resolucion', 
            'direccion', 
            'telefono',
            'fax',
            'email',
            'web',
            'logo',]}),
        ('Configuracion', {'fields': [
            'saludo',
            'informacion_bancaria',
            'control_acudiente',]}),
    ]
    
    list_display = (
        'nombre',
        'nit',         
        'telefono', 
        'web',
        'email'      
    )
    
    inlines = [FuncionarioInline, ]
    search_fields = ('nit',)
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

class InscripcionAdmin(admin.ModelAdmin):
    raw_id_fields = ('ciclo',)
    
    fieldsets = [
        ('Información básica', {'fields': [
            'ciclo',
            'fecha_inicio',
            'fecha_fin',
            ]}),
    ]
    
    list_display = (
        'ciclo',
        'fecha_inicio',         
        'fecha_fin',   
    )
    
    search_fields = ('ciclo',)

class CicloAdmin(ButtonableModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
            'codigo', 
            'fecha_inicio', 
            'fecha_fin',]}),
        ('Configurar inscripciones', {'fields': [
            'fecha_inicio_inscripcion', 
            'fecha_fin_inscripcion',]}),
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
        url = "/admin/academico/ciclo/promocion"
        return HttpResponseRedirect( url )
    promocion.url = "/admin/academico/ciclo/promocion"    #puts this on the end of the admi URL.
    promocion.short_description='Promover ciclo'
    
    buttons = [ promocion, ]


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',         
        'first_name',         
        'last_name',
        'last_login',
        'is_staff'
    )
    
    list_filter = ['is_staff',]

    


#===============================================================================
#AGREGAR VISTAS A INTERFAZ ADMIN 
#===============================================================================
admin.site.register(Calificacion, CalificacionAdmin)
admin.site.register(Ciclo, CicloAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Corte, CorteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(MatriculaCiclo, MatriculaCicloAdmin)
admin.site.register(MatriculaPrograma, MatriculaProgramaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Sede, SedeAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(TipoPrograma, TipoProgramaAdmin)
admin.site.register(TipoNotaConceptual, TipoNotaConceptualAdmin)
admin.site.register(TipoValoracion, TipoValoracionAdmin)
admin.site.register(Profesor, ProfesorAdmin)
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
