# -*- coding: utf-8 -*-
from django.db import models

TIPO_CURSO = (
    ('D', 'Diplomado'),
    ('S', 'Seminario'),
    ('I', 'Intensivo'),
    ('P', 'Personalizado'),
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

class Estudiante(models.Model):
    # Informacion personal  
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True) 
    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO, blank=True) 
    documento = models.CharField(max_length=200, unique=True)
    lugar_expedicion = models.CharField(max_length=200, verbose_name='Lugar expedición', blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=200, blank=True)
    # Informacion de contacto
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=200, blank=True)
    email = models.EmailField(unique=True, blank=True)
    web = models.URLField(blank=True)
    # Informacion de acceso
    usuario = models.CharField(max_length=200, unique=True, blank=True)
    contrasena = models.CharField(verbose_name='Contraseña', max_length=200, blank=True)
    
    def __unicode__(self):
        return self.documento

class Curso(models.Model):
    tipo_curso = models.CharField(max_length=1, choices=TIPO_CURSO, blank=True)
    codigo = models.CharField(verbose_name='Código', max_length=200)
    nombre = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    intensidad = models.IntegerField(help_text='Número de horas.', blank=True, null=True)
    horario = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.codigo
    
class InscripcionCurso(models.Model):
    fecha_inscripcion = models.DateField()
    estudiante = models.ForeignKey(Estudiante)
    curso = models.ForeignKey(Curso)
    codigo = models.CharField(verbose_name='Código', max_length=200)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    nota = models.FloatField(blank=True, null=True)
    
