# -*- coding: utf-8 -*-
from django.db import models
# import Image


ESTADO_ESTUDIANTE = (
    ('A',  'Activo'),
    ('E',  'Egresado'),
    ('X',  'Expulsado'),
    ('R',  'Retirado'),
    ('S',  'Suspendido'),
)


TIPO_DOCUMENTO = (
    ('C',  'Cédula de ciudadania'),
    ('T',  'Tarjeta de identidad'),
    ('P',  'Pasaporte'),
)


SEXO = (
    ('M',  'Masculino'),
    ('F',  'Femenino'),
)


TIPO_REFERENCIA = (
    ('F',  'Familiar'),
    ('P',  'Personal'),
    ('C',  'Comercial'),
    ('A',  'Académica'),
)


JORNADA = (
    ('M',  'Mañana'),
    ('T',  'Tarde'),
    ('N',  'Noche'),
    ('S',  'Sábado'),
    ('D',  'Domingo'),
)


MODULO = (
    ('H',  'Humanidades'),
    ('C',  'Ciencias básicas'),
    ('T',  'Técnico'),
)


PERIODICIDAD = (
    ('H',  'Horas'),
    ('D',  'Dias'),
    ('N',  'Semanas'),
    ('M',  'Meses'),
    ('S',  'Semestres'),
    ('A',  'Años'),
)


DIAS = (
    ('L',  'Lunes'),
    ('M',  'Martes'),
    ('C',  'Miércoles'),
    ('J',  'Jueves'),
    ('V',  'Viernes'),
    ('S',  'Sábado'),
    ('D',  'Domingo'),
)


TIPO_SALON = (
    ('A',  'Aula'),
    ('L',  'Laboratorio'),
    ('U',  'Auditorio'),
    ('I',  'Aire libre'),
    ('O',  'Otro'),
)


TIPO_ESTUDIO = (
    ('S',  'Secundaria'),
    ('T',  'Técnico'),
    ('U',  'Universitario'),
    ('O',  'Otros estudios'),
)


TIPO_PROGRAMA = (
    ('T',  'Técnico'),
    ('A',  'Auxiliar'),
    ('D',  'Diplomado'),
    ('S',  'Seminario'),
    ('I',  'Intensivo'),
)


class Profesor(models.Model):
  # Informacion personal
  nombre = models.CharField(max_length=200)
  apellido = models.CharField(max_length=200)
  sexo = models.CharField(max_length=1, choices=SEXO) 
  tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO) 
  documento = models.CharField(max_length=200, unique = True)
  lugar_expedicion = models.CharField(max_length=200, blank = True)
  fecha_nacimiento = models.DateField()
  lugar_nacimiento = models.CharField(max_length=200)
  direccion = models.CharField(max_length=200)
  lugar_residencia = models.CharField(max_length=200)
  telefono = models.CharField(max_length=200)
  email = models.EmailField(unique = True)
  web = models.URLField(blank=True)
  foto = models.CharField(max_length=200, blank=True)
  
  def __unicode__(self):
    salida = self.apellido + ', ' + self.nombre
    return salida

class Estudiante(models.Model):
  # Informacion personal  
  nombre = models.CharField(max_length=200)
  apellido = models.CharField(max_length=200)
  sexo = models.CharField(max_length=1, choices=SEXO) 
  tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO) 
  documento = models.CharField(max_length=200, unique = True)
  lugar_expedicion = models.CharField(max_length=200, blank = True)
  fecha_nacimiento = models.DateField()
  lugar_nacimiento = models.CharField(max_length=200)
  direccion = models.CharField(max_length=200)
  lugar_residencia = models.CharField(max_length=200)
  telefono = models.CharField(max_length=200)
  email = models.EmailField(unique = True)
  web = models.URLField(blank=True)
  foto = models.CharField(max_length=200, blank=True)


class OtrosEstudios(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  tipo_estudio = models.CharField(max_length=1, choices=TIPO_ESTUDIO, blank = True) 
  institucion = models.CharField(max_length=200, blank = True)
  titulo = models.CharField(max_length=200, blank = True)
  fecha_graduacion = models.DateField(blank = True)


class Referencia(models.Model):
  estudiante = models.ForeignKey(Estudiante)
  tipo_referencia = models.CharField(max_length=1, choices=TIPO_REFERENCIA, blank = True) 
  nombre = models.CharField(max_length=200, blank = True)
  tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO, blank = True)
  documento = models.CharField(max_length=200, blank = True)
  ciudad_expedicion = models.CharField(max_length=200, blank = True)
  direccion = models.CharField(max_length=200, blank = True)
  telefono = models.CharField(max_length=200, blank = True)

  
class Salon(models.Model):
  codigo = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=200, blank = True)
  capacidad = models.IntegerField(blank = True)
  tipo_salon = models.CharField(max_length=1, choices=TIPO_SALON, blank = True)
  
  def __unicode__(self):
    return self.codigo
  
  
class Programa(models.Model):
  tipo_programa = models.CharField(max_length=1, choices=TIPO_PROGRAMA)
  codigo = models.CharField(max_length=200)
  nombre = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=200, blank = True)
  titulo = models.CharField(max_length=200, help_text = "Título otorgado al finalizar el programa.")
  resolucion = models.CharField(max_length=200, help_text = "Acto administrativo que valida este programa.", blank = True)  
  actitudes = models.TextField(max_length=200, help_text = "Actitudes requeridas para los aspirantes.", blank = True)  
  perfil_profesional = models.TextField(max_length=200, help_text = "Perfil profesional del egresado.", blank = True)
  funciones = models.TextField(max_length=200, help_text = "Funciones en las que se puede desempeñar el egresado.", blank = True)  
  periodicidad = models.CharField(max_length=1, choices=PERIODICIDAD) 
  duracion = models.IntegerField()
  jornada = models.CharField(max_length=1, choices=JORNADA)
  
  def __unicode__(self):
    r = self.nombre + ' - ' + self.jornada.long_description
    return r
  

class MatriculaEstudiante(models.Model):
  # Informacion general
  fecha_inscripcion = models.DateField()
  estudiante = models.ForeignKey(Estudiante)
  estado = models.CharField(max_length=1, choices=ESTADO_ESTUDIANTE, default = 'A')
  programa = models.ForeignKey(Programa)
  usuario = models.CharField(max_length=200, unique = True)
  contrasena = models.CharField(max_length=200)
  codigo = models.CharField(max_length=200, unique = True)
  
  def __unicode__(self):
    return self.codigo


class Pago(models.Model):
  estudiante = models.ForeignKey(MatriculaEstudiante)
  fecha_pago = models.DateField()
  valor = models.FloatField()
  recibo_caja = models.CharField(max_length=200)
  observaciones = models.TextField(max_length=200, blank = True)
  
  
class Competencia(models.Model):
  programa = models.ForeignKey(Programa)
  codigo = models.CharField(max_length=200)
  nombre = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=200, blank = True)
  modulo = models.CharField(max_length=1, choices=MODULO)
  periodo = models.IntegerField(help_text = "Nivel en el cual se debe ver esta competencia.")
    
  def __unicode__(self):
    return self.codigo
  
  
class Amonestacion(models.Model):
  estudiante = models.ForeignKey(MatriculaEstudiante)
  profesor = models.ForeignKey(Profesor)
  competencia = models.ForeignKey(Competencia)
  fecha_amonestacion = models.DateField()
  motivo = models.TextField(max_length=200, blank = True, help_text = "Motivo por el cual se hace el llamado de atención.")

  
class Curso(models.Model):
  competencia = models.ForeignKey(Competencia)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  profesor = models.ForeignKey(Profesor)
  grupo = models.IntegerField(help_text = "Número del grupo 1, 2, 3, ...")
  numero_estudiantes = models.IntegerField(help_text = "Número esperado de estudiantes.", blank = True)
  
  def __unicode__(self):
    salida = self.competencia.codigo + '-' + self.grupo
    return salida
    

class MatriculaCurso(models.Model):
  curso = models.ForeignKey(Curso)
  estudiante = models.ForeignKey(MatriculaEstudiante)
  nota = models.FloatField(blank = True)


class Sesion(models.Model):
  curso = models.ForeignKey(Curso)
  dia = models.CharField(max_length=1, choices=DIAS) 
  hora_inicio = models.TimeField()
  hora_fin = models.TimeField()
  salon = models.ForeignKey(Salon)