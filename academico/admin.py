# -*- coding: utf-8 -*-
from academico.models import Ciclo, NotaCorte, MatriculaCiclo, Calificacion, Corte, Programa, Salon, Competencia, EstudioComplementario, Referencia, MatriculaPrograma, Amonestacion, Estudiante, Profesor, HorarioCurso, Curso, Institucion, Funcionario
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
    fields = ('curso', 'nota_definitiva', 'nota_habilitacion', 'perdio_fallas')
    readonly_fields = ('nota_definitiva', 'nota_habilitacion')


class MatriculaCicloAdmin(ButtonableModelAdmin):
    raw_id_fields = ('matricula_programa', 'ciclo')
    fieldsets = [
        ('Información básica', {'fields': [
            'fecha_inscripcion', 
            'matricula_programa',
            'ciclo',
            'promedio_ciclo',
            'observaciones']}),
    ]
    list_display = (
        'codigo_estudiante',
        'nombre_estudiante',
        'nombre_programa',
        'promedio_ciclo',
        'puesto',
        'ciclo',
        'fecha_inscripcion',
    )
    readonly_fields = ('promedio_ciclo',)
    
    inlines = [CalificacionInline]
    list_filter = ['fecha_inscripcion', 'ciclo']
    search_fields = ('matricula_programa__programa__id', )
    date_hierarchy = 'fecha_inscripcion'
    
    def constancia(self, obj):
        url = "/admin/academico/matriculaciclo/constancia"
        return HttpResponseRedirect( url )
    constancia.url = "/admin/academico/matriculaciclo/constancia"    #puts this on the end of the admin URL.
    constancia.short_description='Imprimir constancia'
    
    buttons = [constancia, ]


class NotaCorteInline(admin.TabularInline):
    raw_id_fields = ('corte',)
    model = NotaCorte
    extra = 1


class CalificacionAdmin(admin.ModelAdmin):
    raw_id_fields = ('curso', 'matricula_ciclo')
    
    fieldsets = [
        ('Información básica', {'fields': [
            'curso', 
            'matricula_ciclo',
            'codigo_ciclo',
            'nota_definitiva', 
            'nota_habilitacion',
            'perdio_fallas',
            ]}),
    ]
    inlines = [NotaCorteInline]
    list_display = (
        'nombre_competencia', 
        'nombre_estudiante', 
        'codigo_ciclo',
        'nota_definitiva', 
        'nota_habilitacion',
        'fallas',
        'perdio_fallas',
    )
    
    readonly_fields = ('nota_definitiva', 'codigo_ciclo')
    search_fields = ['matricula_ciclo__ciclo__codigo', 'curso__competencia__nombre', 
                     'matricula_ciclo__matricula_programa__estudiante__nombre1', 'matricula_ciclo__matricula_programa__estudiante__nombre2', 
                     'matricula_ciclo__matricula_programa__estudiante__apellido1', 'matricula_ciclo__matricula_programa__estudiante__apellido2',]
#    matricula_ciclo__matricula_programa__estudiante__nombre1


class ProgramaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [     
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
        ('Información básica', {'fields': [
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
    raw_id_fields = ('ciclo', 'competencia', 'profesor')
    fields = ('grupo', 'competencia', 'profesor', 'ciclo')


class CompetenciaInline(admin.TabularInline):
    model = Competencia
    extra = 1
    raw_id_fields = ('codigo', 'programa', 'nombre')
    fields = ('grupo', 'profesor', 'ciclo')


class CompetenciaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
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
                                   'estado',
                                   'promedio_acumulado',
                                   'becado',
                                   ]}),
                 ]
    
    list_display = (
                    'codigo',
                    'nombre_estudiante',
                    'nombre_programa',
                    'promedio_acumulado',
                    'fecha_inscripcion',
                    'estado'
                    )
    
    date_hierarchy = 'fecha_inscripcion'
    
    readonly_fields = ('promedio_acumulado',)
    
    list_filter = ['estado', 'programa']
    search_fields = ('codigo', 'programa__nombre', 'estado__nombre', 'estudiante__nombre1', 'estudiante__apellido1')
    
    def inscritos(self, request, obj):
        obj.inscritos()
    inscritos.url = "/admin/academico/matriculaprograma/inscritos"
    inscritos.short_description='Detalle inscritos'
    
    def consolidadoInscritos(self, request, obj):
        obj.consolidadoInscritos()
    consolidadoInscritos.url = "/admin/academico/matriculaprograma/consolidadoinscritos"
    consolidadoInscritos.short_description='Consolidado inscritos'
    
    buttons_list = [inscritos, consolidadoInscritos, ]
    
    def imprimircarnet(self, request, obj):
        obj.imprimirCarnet()
        
    imprimircarnet.short_description='Imprimir Carnet'
    
    buttons = [imprimircarnet, ]



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
        ('Información básica', {'fields': [
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
        'corte_actual'        
    )
    search_fields = ('codigo_corte',)
    date_hierarchy = 'fecha_inicio'
    

class FuncionarioInline(admin.TabularInline):
    model = Funcionario
    extra = 1
    fields = ('nombre', 'tipo_documento', 'documento', 'lugar_expedicion', 'tipo_funcionario')

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
    ]
    
    list_display = (
        'nombre',
        'nit',         
        'telefono', 
        'web',
        'email'      
    )
    
    inlines = [FuncionarioInline,]
    search_fields = ('nit',)
    


class CicloAdmin(ButtonableModelAdmin):
    fieldsets = [
        ('Información básica', {'fields': [
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
        url = "/admin/academico/ciclo/promocion"
        return HttpResponseRedirect( url )
    promocion.url = "/admin/academico/ciclo/promocion"    #puts this on the end of the admin URL.
    promocion.short_description='Promover ciclo'
    
    buttons = [ promocion, ]

#===============================================================================
#AGREGAR VISTAS A INTERFAZ ADMIN 
#===============================================================================
admin.site.register(Calificacion, CalificacionAdmin)
admin.site.register(Ciclo, CicloAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Corte, CorteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(MatriculaCiclo, MatriculaCicloAdmin)
admin.site.register(MatriculaPrograma, MatriculaProgramaAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Profesor, ProfesorAdmin)