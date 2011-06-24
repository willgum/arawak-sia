from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    #urls para docentes
    (r'^$', indice),
    (r'^docente/$', indice),
    (r'^docente/programas/$', programasDocente),
        
    (r'^docente/horarios/$', horariosDocente),
    (r'^docente/horarios/(?P<materia_id>\d+)/$', materiasDocente),
    
    (r'^docente/notas/$', notasDocente), 
    (r'^docente/notas/(?P<materia_id>\d+)/$', materiasDocente),
    (r'^docente/notas/guardar/(?P<ciclo_id>\d+)/(?P<curso_id>\d+)/$', guardarNotasDocente),
    
    (r'^docente/notas/guardar/\d+/\d+/nota/$', guardarNotaDocente),
    (r'^docente/notas/guardar/\d+/\d+/falla/$', guardarFallaDocente),
    (r'^docente/notas/guardar/\d+/\d+/fallas/$', guardarFallas),
    (r'^docente/notas/guardar/\d+/\d+/valoracion/$', guardarValoracion),
    (r'^docente/notas/guardar/\d+/\d+/horas/$', guardarHoras),
    
    #urls para estudiantes
    (r'^$', indice),
    (r'^estudiante/$', indice),
    (r'^estudiante/programas/$', programasEstudiante),

    (r'^estudiante/horarios/$', horariosEstudiante),
    (r'^estudiante/horarios/(?P<materia_id>\d+)/$', materiasDetalleEstudiante),
    
    (r'^estudiante/notas/$', notasEstudiante),
    (r'^estudiante/notas/(?P<materia_id>\d+)/$', materiasDetalleEstudiante),
    
    (r'^estudiante/historial/$', historialEstudiante),
    (r'^estudiante/historial/(?P<materia_id>\d+)/$', materiasDetalleEstudiante),
    
    (r'^estudiante/inscripcion/$', inscripcionMaterias),
    (r'^estudiante/inscripcion/inscribir/$', inscribirMateria),
    
)