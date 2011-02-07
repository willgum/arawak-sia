from django.conf.urls.defaults import *
from academico.views import *

urlpatterns = patterns('',
    #urls para docentes
    (r'^$', indice),
    (r'^docente/$', indice),
    (r'^docente/programas/$', programasDocente),
    
    (r'^docente/competencias/$', competenciasDocente), 
    (r'^docente/competencias/(?P<competencia_id>\d+)/$', competenciasDetalleDocente),
        
    (r'^docente/horarios/$', horariosDocente),
    (r'^docente/horarios/(?P<competencia_id>\d+)/$', competenciasDetalleDocente), 
    
    (r'^docente/notas/$', notasDocente), 
    (r'^docente/notas/(?P<competencia_id>\d+)/$', competenciasDetalleDocente),
    (r'^docente/notas/guardar/(?P<curso_id>\d+)/$', guardarNotasDocente),
    
    (r'^docente/notas/guardar/\d+/nota/$', guardarNotaDocente),
    (r'^docente/notas/guardar/\d+/falla/$', guardarFallasDocente),
    
    #urls para estudiantes
    (r'^$', indice),
    (r'^$estudiante/', indice),
    (r'^estudiante/programas/$', programasEstudiante),
    
    (r'^estudiante/competencias/$', competenciasEstudiante), 
    (r'^estudiante/competencias/(?P<competencia_id>\d+)/$', competenciasDetalleEstudiante),
    
    (r'^estudiante/horarios/$', horariosEstudiante),
    (r'^estudiante/horarios/(?P<competencia_id>\d+)/$', competenciasDetalleEstudiante), 
    
    (r'^estudiante/notas/$', notasEstudiante),
)