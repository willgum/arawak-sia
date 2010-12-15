# -*- coding: utf-8 -*-
from django.db import models

# TODO: Leer configuracion desde un archivo externo,
# p.e., valores de constantes.
# http://docs.python.org/library/configparser.html

TIPO_COMPORTAMIENTO = (
  ('E', 'Excelente'),
  ('B', 'Bueno'),
  ('A', 'Aceptable'),
  ('I', 'Insuficiente'),
  ('N', 'No aplica'),
)

ESTADO_INSCRIPCION = (
  ('A', 'Activo'),
  ('E', 'Egresado'),
  ('X', 'Expulsado'),
  ('R', 'Retirado'),
  ('D', 'Suspendido disciplina')
)

TIPO_DOCUMENTO = (
  ('C', 'Cédula de ciudadania'),
  ('T', 'Tarjeta de identidad'),
  ('P', 'Pasaporte'),
)

SEXO = (
  ('M', 'Masculino'),
  ('F', 'Femenino'),
)

TIPO_REFERENCIA = (
  ('F', 'Familiar'),
  ('P', 'Personal'),
  ('C', 'Comercial'),
  ('A', 'Académica'),
  ('L', 'Laboral'),
)

JORNADA = (
  ('M', 'Mañana'),
  ('T', 'Tarde'),
  ('N', 'Noche'),
  ('S', 'Sábado'),
  ('D', 'Domingo'),
)

MODULO = (
  ('H', 'Humanidades'),
  ('C', 'Ciencias básicas'),
  ('T', 'Técnico'),
)

PERIODICIDAD = (
  ('H', 'Horas'),
  ('D', 'Días'),
  ('N', 'Semanas'),
  ('M', 'Meses'),
  ('S', 'Semestres'),
  ('A', 'Años'),
)

DIAS = (
  ('L', 'Lunes'),
  ('M', 'Martes'),
  ('C', 'Miércoles'),
  ('J', 'Jueves'),
  ('V', 'Viernes'),
  ('S', 'Sábado'),
  ('D', 'Domingo'),
)

TIPO_SALON = (
  ('A', 'Aula'),
  ('L', 'Laboratorio'),
  ('U', 'Auditorio'),
  ('I', 'Aire libre'),
  ('M', 'Aula mantenimiento'),
  ('O', 'Otro'),
)

TIPO_ESTUDIO = (
  ('P', 'Primaria'),
  ('S', 'Secundaria'),
  ('T', 'Técnico'),
  ('U', 'Universitario'),
  ('E', 'Especialización'),
  ('M', 'Maestría'),
  ('D', 'Doctorado'),
  ('O', 'Otros estudios'),
)

TIPO_PROGRAMA = (
  ('T',  'Técnico'),
  ('A',  'Auxiliar'),
  ('D',  'Diplomado'),
  ('S',  'Seminario'),
  ('I',  'Intensivo'),
  ('P',  'Personalizado'),
)

class Profesor(models.Model):
  # Informacion personal
  nombre = models.CharField(max_length=200)
  apellido = models.CharField(max_length=200)
  sexo = models.CharField(max_length=1, choices=SEXO, blank=True) 
  tipo_documento = models.CharField(max_length=1, 
  	                                choices=TIPO_DOCUMENTO,
  	                                blank=True) 
  documento = models.CharField(max_length=200, unique = True)
  lugar_expedicion = models.CharField(verbose_name='Lugar expedición', 
                                      max_length=200, 
                                      blank=True)
  fecha_nacimiento = models.DateField(blank=True, null=True)
  lugar_nacimiento = models.CharField(blank=True, max_length=200)
  foto = models.FileField(upload_to='/', blank=True)
  # Informacion de contacto
  direccion = models.CharField(verbose_name='Dirección', 
                               max_length=200,
                               blank=True)
  lugar_residencia = models.CharField(max_length=200, blank=True)
  telefono = models.CharField(verbose_name='Teléfono', 
                              max_length=200,
                              blank=True)
  email = models.EmailField(unique = True, blank=True)
  web = models.URLField(blank=True)
  # Informacion de acceso
  usuario = models.CharField(max_length=200, 
                             unique = True,
                             blank=True)
  contrasena = models.CharField(verbose_name='Contraseña', 
                                max_length=200,
                                blank=True)
  
  def __unicode__(self):
    return self.documento
    
  class Meta:
    verbose_name_plural = 'profesores'


class ExperienciaLaboralProfesor(models.Model):
  profesor = models.ForeignKey(Profesor)
  cargo = models.CharField(max_length=200, blank=True)
  empresa = models.CharField(max_length=200, blank=True)
  fecha_inicio = models.DateField(blank=True, null=True)
  fecha_fin = models.DateField(blank=True, null=True)
  actualmente = models.BooleanField()
  
  class Meta:
    verbose_name_plural = 'experiencia laboral profesores'


class OtrosEstudiosProfesor(models.Model):
  profesor = models.ForeignKey(Profesor)
  tipo_estudio = models.CharField(max_length=1, 
                                  choices=TIPO_ESTUDIO, 
                                  blank=True)
  institucion = models.CharField(verbose_name='Institución', 
                                  max_length=200, 
                                  blank=True)
  titulo = models.CharField(verbose_name='Título', 
                            max_length=200, 
                            blank=True)
  fecha_graduacion = models.DateField(verbose_name='Fecha graduación', 
                                      blank=True,
                                      null=True)

  class Meta:
    verbose_name_plural = 'otros estudios profesores'


class Salon(models.Model):
  codigo = models.CharField(verbose_name='Código', max_length=200)
  descripcion = models.TextField(verbose_name='Descripción', 
                                max_length=200, 
                                blank=True)
  capacidad = models.IntegerField(blank=True)
  tipo_salon = models.CharField(verbose_name='Tipo salón', 
                                max_length=1, 
                                choices=TIPO_SALON, 
                                blank=True)
  
  def __unicode__(self):
    return self.codigo

  class Meta:
    verbose_name_plural = 'salones'


class Programa(models.Model):
  # Informacion general
  tipo_programa = models.CharField(max_length=1, 
                                    choices=TIPO_PROGRAMA,
                                    blank=True)
  codigo = models.CharField(verbose_name='Código', 
                            max_length=200)
  nombre = models.CharField(max_length=200, blank=True)
  descripcion = models.TextField(verbose_name='Descripción', 
                                  max_length=200, 
                                  blank=True)
  titulo = models.CharField(verbose_name='Título', 
                            max_length=200, 
                            help_text='Título otorgado al finalizar el programa.',
                            blank=True)
  resolucion = models.CharField(verbose_name='Resolución', 
                                max_length=200, 
                                help_text="Acto administrativo que valida este programa.", 
                                blank=True)
  # Horario
  periodicidad = models.CharField(max_length=1, 
                                  choices=PERIODICIDAD,
                                  blank=True) 
  duracion = models.IntegerField(verbose_name='Duración', 
                                 blank=True,
                                 null=True)
  jornada = models.CharField(max_length=1, 
                              choices=JORNADA,
                              blank=True)
  # Informacion adicional
  actitudes = models.TextField(max_length=200, 
                                help_text="Actitudes requeridas para los aspirantes.", 
                                blank=True)
  perfil_profesional = models.TextField(max_length=200, 
                                        help_text="Perfil profesional del egresado.", 
                                        blank=True)
  funciones = models.TextField(max_length=200, 
                                help_text="Funciones en las que se puede desempeñar el egresado.", 
                                blank=True)
  
  def __unicode__(self):
  	return self.codigo


class Estudiante(models.Model):
  # Informacion personal  
  nombre = models.CharField(max_length=200)
  apellido = models.CharField(max_length=200)
  sexo = models.CharField(max_length=1, 
                          choices=SEXO,
                          blank=True) 
  tipo_documento = models.CharField(max_length=1, 
                                    choices=TIPO_DOCUMENTO,
                                    blank=True) 
  documento = models.CharField( max_length=200, 
                                unique = True)
  lugar_expedicion = models.CharField(max_length=200, 
                                      verbose_name='Lugar expedición',
                                      blank=True)
  fecha_nacimiento = models.DateField(blank=True, null=True)
  lugar_nacimiento = models.CharField(max_length=200, blank=True)
  # Requisitos
  fotocopia_documento = models.FileField(upload_to='/', blank=True)
  fotocopia_diploma = models.FileField(upload_to='/', blank=True)
  foto = models.FileField(upload_to='/', blank=True)
  # Informacion de contacto
  direccion = models.CharField( verbose_name='Dirección',
                                max_length=200,
                                blank=True)
  lugar_residencia = models.CharField(max_length=200, blank=True)
  telefono = models.CharField(verbose_name='Teléfono',
                              max_length=200,
                              blank=True)
  email = models.EmailField(unique = True, blank=True)
  web = models.URLField(blank=True)
  # Informacion de acceso
  usuario = models.CharField(max_length=200, 
                             unique = True,
                             blank=True)
  contrasena = models.CharField(verbose_name='Contraseña',
                                max_length=200,
                                blank=True)
  
  def __unicode__(self):
    return self.documento


class OtrosEstudiosEstudiante(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  tipo_estudio = models.CharField(max_length=1, 
                                  choices=TIPO_ESTUDIO, 
                                  blank=True) 
  institucion = models.CharField( verbose_name='Institución', 
                                  max_length=200, 
                                  blank=True)
  titulo = models.CharField(verbose_name='Título', 
                            max_length=200, 
                            blank=True)
  fecha_graduacion = models.DateField(verbose_name='Fecha graduación', 
                                      blank=True, 
                                      null=True)


class Referencia(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  tipo_referencia = models.CharField( max_length=1, 
                                      choices=TIPO_REFERENCIA, 
                                      blank=True) 
  nombre = models.CharField(max_length=200, blank=True)
  tipo_documento = models.CharField(max_length=1, 
                                    choices=TIPO_DOCUMENTO, 
                                    blank=True)
  documento = models.CharField(max_length=200, blank=True)
  direccion = models.CharField( verbose_name='Dirección',
                                max_length=200, 
                                blank=True)
  telefono = models.CharField(verbose_name='Teléfono',
                              max_length=200, 
                              blank=True)


class InscripcionEstudiante(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
  programa = models.ForeignKey(Programa)
  codigo = models.CharField(verbose_name='Código',
                            max_length=200, 
                            unique = True)
  estado = models.CharField(max_length=1, 
                            choices=ESTADO_INSCRIPCION, 
                            default='A')
  fecha_vencimiento = models.DateField()
  becado = models.BooleanField(help_text='Indica si el estudiante recibe o no beca.')
  promedio_acumulado = models.FloatField(blank=True, null=True)
  
  def __unicode__(self):
    return self.codigo


class Competencia(models.Model):
  programa = models.ForeignKey(Programa)
  codigo = models.CharField(verbose_name='Código', 
                            max_length=200)
  nombre = models.CharField(max_length=200, blank=True)
  descripcion = models.TextField( verbose_name='Descripción', 
                                  max_length=200, 
                                  blank=True)
  modulo = models.CharField(verbose_name='Módulo', 
                            max_length=1, 
                            choices=MODULO,
                            blank=True)
  periodo = models.IntegerField(help_text='Nivel en el cual se debe ver esta competencia.',
                                blank=True,
                                null=True)
  intensidad = models.IntegerField(help_text='Número de horas requeridas para dictar la compentencia.',
                                   blank=True,
                                   null=True)
  
  def __unicode__(self):
    return self.codigo
  
  
class MatriculaPrograma(models.Model):
  fecha_expedicion = models.DateField()
  inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
  programa = models.ForeignKey(Programa)
  fecha_vencimiento = models.DateField(blank=True, null=True)
  promedio_periodo = models.FloatField(blank=True, null=True)
  puesto = models.IntegerField(help_text='Puesto ocupado durante el periodo academico.',
                               blank=True,
                               null=True)
  observaciones = models.TextField(max_length=200, blank=True)
  

class Amonestacion(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  profesor = models.ForeignKey(Profesor)
  competencia = models.ForeignKey(Competencia)
  fecha = models.DateField()
  motivo = models.TextField(max_length=200, 
                            blank=True, 
                            help_text='Motivo por el cual se hace el llamado de atención.')

  class Meta:
    verbose_name_plural = 'amonestaciones'
    
    
class Curso(models.Model):
  competencia = models.ForeignKey(Competencia)
  codigo = models.CharField(verbose_name='Código', 
                            max_length=200)
  fecha_inicio = models.DateField(blank=True, null=True)
  fecha_fin = models.DateField(blank=True, null=True)
  profesor = models.ForeignKey(Profesor)
  grupo = models.IntegerField(help_text='Número del grupo 1, 2, 3, ...',
                              blank=True,
                              null=True)
  estudiantes = models.IntegerField(help_text='Número esperado de estudiantes.', 
                                    blank=True,
                                    null=True)
  
  def __unicode__(self):
    return self.codigo


class MatriculaCurso(models.Model):
  curso = models.ForeignKey(Curso)
  inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
  nota_definitiva = models.FloatField(blank=True)
  nota_habilitacion = models.FloatField(verbose_name='Nota habilitación', 
                                        blank=True)
  perdio_fallas = models.BooleanField(verbose_name='Perdió por fallas')


class Corte(models.Model):
  codigo = models.CharField(max_length=200)
  porcentaje = models.IntegerField( help_text="Ingrese un número entre 1 y 100.", 
                                    blank=True)
  fecha_inicio = models.DateField(blank=True, null=True)
  fecha_fin = models.DateField(blank=True, null=True)
  
  def __unicode__(self):
    return self.codigo


class NotaCorte(models.Model):
  matricula_curso = models.ForeignKey(MatriculaCurso)
  corte = models.ForeignKey(Corte)
  nota = models.FloatField(blank=True, null=True)
  fallas = models.IntegerField( help_text="Número de fallas durante el corte.", 
                                blank=True)
  comportamiento = models.CharField(max_length=1, 
                                    choices=TIPO_COMPORTAMIENTO,
                                    blank=True) 

  
class HorarioCurso(models.Model):
  curso = models.ForeignKey(Curso)
  dia = models.CharField( verbose_name='Día', 
                          max_length=1, 
                          choices=DIAS) 
  hora_inicio = models.TimeField()
  hora_fin = models.TimeField()
  salon = models.ForeignKey(Salon, verbose_name='Salón')


class SesionCurso(models.Model):
  curso = models.ForeignKey(Curso)
  hora_inicio = models.DateTimeField(blank=True, null=True)
  hora_fin = models.DateTimeField(blank=True, null=True)


class Asistencia(models.Model):
  sesion_curso = models.ForeignKey(SesionCurso)
  inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
  asistio = models.BooleanField(verbose_name='Asistío', default=True)
  observaciones = models.TextField( max_length=200, 
                                    blank=True)